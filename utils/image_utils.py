import os
import pandas as pd
import numpy as np
from PIL import Image
import time


class ImageUtilities:
    def __init__(self, image):
        self.image = image

    def orientation_check(self, single_image) -> str:
        '''
        Checks if the image is landscape or portrait 
        by comparing the width and height.
        '''
        size = single_image.size
        if size[0] > size[1]:
            return "landscape"
        else:
            return "portrait"

    def double_split(self, original, a_side, b_side, output_folder):
        '''
        Splits the image into two images based on the binding point.
        '''
        DOWNSCALED_WIDTH = 400
        img = self.downscale(original)
        df = self.pixels_df(img)
        # 0 = white, 1 = black pixels
        contrasted = df.applymap(lambda x: int(np.sqrt(x) if x < 127 else x ** 2) / (255 ** 2))
        means = self.middle(contrasted, np.nan).mean()

        apply_func = self.apply_func_factory(means)

        center_amplifier = means.reset_index().apply(apply_func, axis=1)

        low_std_amplifier = self.rescale(means / (1 - means.std()))
        signal = self.rescale(self.rescale(means) * center_amplifier * low_std_amplifier)
        normalized = (signal * 10).round()
        grouped = pd.DataFrame([normalized]).T.groupby(normalized, as_index=False)

        # luminosity distinct sorted values (10 at max = whitest)
        lum_val = grouped[0].last().round().values.flatten()
        lum_val.sort()

        file_path = '{}/{}.jpg'
        left_file_path, right_file_path = file_path.format(output_folder, a_side), file_path.format(output_folder, b_side)

        if len(lum_val) == 0:
            width = original.size[0]/2
            self.horizontal_split(original, width, left_file_path, right_file_path)
            return

        # whitests columns (maximum of luminosity)
        whitest = lum_val[-1]
        darkest = lum_val[0]
        white_cols = pd.Series(grouped.get_group(whitest).index)
        dark_cols = pd.Series(grouped.get_group(darkest).index)

        if len(white_cols) < 0.01 * DOWNSCALED_WIDTH and lum_val[-2] >= whitest - 1:
            next_group = pd.Series(grouped.get_group(lum_val[-2]).index)
            if len(next_group) < 0.02 * DOWNSCALED_WIDTH:
                white_cols = white_cols._append(next_group).sort_values()

        first_idx, last_idx = white_cols.min(), white_cols.max()

        white_band = normalized.loc[first_idx:last_idx]
        if white_band.min() > white_band.max() - 2:
            margin = max(1, round(0.01 * DOWNSCALED_WIDTH))
            white_band = normalized.loc[first_idx - margin:last_idx + margin]

        # we have a dark local minimum in the white band
        band_min = white_band.min()
        if whitest == 10 and (last_idx - first_idx + 1) == len(white_cols) and len(white_cols) >= 0.02 * DOWNSCALED_WIDTH:
            binding_point = white_cols.median()
        elif band_min <= whitest - 5:
            dark_inside_median = white_band[white_band == band_min].reset_index()['index']

            binding_point = dark_inside_median.median()
        elif darkest == 0 and len(dark_cols) <= 0.01 * DOWNSCALED_WIDTH:
            binding_point = dark_cols.median()
        else:
            # binding as median of indexes
            binding_point = white_cols.median()
        o_width, _ = original.size
        cut_x = round(o_width * (binding_point / DOWNSCALED_WIDTH))
        self.horizontal_split(original, cut_x, left_file_path, right_file_path)
    

    def pixels_df(self):
        '''
        Returns a dataframe of the pixels of the image.
        '''
        pixels = np.array(self.image)
        pixels_df = pd.DataFrame(pixels)
        return pixels_df
    
    def downscale(self):
        '''
        Returns a downsampled image.
        '''
        o_width, o_height = self.image.size
        height = round(400 / o_width) * o_height
        ds_img = self.image.convert('L').resize((400, height), resample=Image.BILINEAR)
        return ds_img
    
    def middle(self, df, replacement):
        df2 = df.copy()
        if df.__class__ == pd.DataFrame:
            third = int(len(df.columns) / 3)
            df2.loc[:, :third] = replacement
            df2.loc[:, 2*third:] = replacement
        else:
            third = int(len(df) / 3)
            df2.loc[:third] = replacement
            df2.loc[2*third:] = replacement
        return df2
    
    def rescale(self, serie):
        serie -= serie.min()
        return serie / serie.max()
    
    def apply_func_factory(self, serie):
        center = len(serie) / 2
        def apply_func(x):
            idx = x.name
            return 1 - (abs(center - idx) ** 1.618) / center ** 1.618
        return apply_func


