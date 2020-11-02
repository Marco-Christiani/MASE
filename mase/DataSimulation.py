#!/usr/bin/env python

# !pip install pyplot-themes # run me if pyplot_themes import fails
import pandas as pd
import numpy as np
import warnings


class Simulation:
    def __init__(self, n_observations, means: np.ndarray = None, covariance_matrix: np.ndarray = None):
        # Flag value that indicates function use, not method use
        # Therefore, we set a flag and immediately return
        if n_observations == -1:
            self.initialized = False
            return
        self.initialized = True
        self.covariance_matrix = covariance_matrix
        self.means = means

        self.n = n_observations
        n_features = self.n
        if means is not None:
            n_features = len(means)
        if covariance_matrix is not None:
            n_features = len(covariance_matrix)

        if covariance_matrix is None:
            self.covariance_matrix = np.eye(n_features)
        if means is None:
            self.means = np.zeros(n_features)

        self.df = self._generate_data()

    def _generate_data(self):
        result = np.random.multivariate_normal(self.means,
                                               self.covariance_matrix,
                                               size=self.n)
        return pd.DataFrame(result)

    def _check_initialized(self, df):
        """
        Checks to see if a Simulation object has been created. Since some methods are exposed as functions,
        this is meant to detect if a user calls a function without passing a df argument.
        The intended use of this module is to either (1) create a Simulation object if simulating data from scratch
        or (2) to use the exposed methods as functions and pass existing data as the df paramter
        :return:
        """
        if df is None:
            if not self.initialized:
                raise Exception(
                    'Please either (1) supply the `df` parameter if you have existing data or (2) initialize a '
                    'Simulation object.')
            return self.df  # User did not pass df and Simulation obj is initialized, this is the correct usage

        elif self.initialized:
            # df NOT None and Sim obj is initialized
            warnings.warn('Attempted to pass a `df` argument to a method of an initialized Simulation object. Will '
                          'default to the object\'s stored `df` attribute. If you wish to use a different `df` '
                          'please use the function instead of the method.')
            return self.df  # If user passes df even though Simulation was initialized

    def add_mean_drift(self, shifts_df, df=None):
        """
        *THIS METHOD IS DEPRECATED*
        Gradually shifts mean over time.
        This method uses the shifts_df parameter to give more control ovAer the rate at
        which the drift takes place. For example, a "rough" drift might include many
        small shifts in mean, along with a few larger shifts. Alternatively, to
        simulate a "smooth" drift, one can use the NumPy method
        `linspace(start, stop, num)` to build shift_df to create equal mean shifts
        over a specified interval starting at `start` ending at `end` with `num` steps.

        Args:
        df: DataFrame
            Data with features as columns and rows as observations.

        shifts_df: DataFrame
            Column names (as ints) correspond to feature indexes in df.
            Rows contain series of individual mean targets that are multiples of a
            column's standard deviation.
            i.e.
            --------------
            |   1   |   3  |
            |--------------|
            | 3.11  | 1.25 |
            | 3.21  | 1.30 |
            | 5.29  | 1.35 |
            --------------
            This data frame results in feature 1's mean being shifted to 3.11 sd's
            then 3.21 sd's then 5.29 sd's each by adding 1 observation to feature 1.
            Feature 3 is shifted to 1.25 sd's then 1.30 sd's, then 1.35 sd's each by
            adding 1 observation to feature 3.
        """
        df = self._check_initialized(df)

        local_df = df.copy(deep=True)
        feature_indexes = shifts_df.columns.values

        n_observations = local_df.shape[0]

        def val_needed_for_shift(data_list, target_mean, sd, mean):
            # print(f'Calculated mean target: mean+target*sd = {np.mean(data_list)}\
            # +{target_mean}*{sd}={np.mean(data_list)+sd*target_mean}\n')
            target_mean = mean + sd * target_mean
            needed_val = (len(data_list) + 1) * target_mean - sum(data_list)
            return needed_val

        sd_df = local_df[feature_indexes].std(
        )  # Save original std dev of columns
        means_df = local_df[feature_indexes].mean(
        )  # Save original means of columns
        for index, row in shifts_df.iterrows(
        ):  # iterate over rows of shift_df
            column_data = local_df[
                feature_indexes]  # extract feature columns to be shifted
            # Calculate size of point to add to induce desired mean shift
            # feature_means = column_data.mean()
            new_obs_list = []
            i = 0
            for col in column_data.columns:
                target_mean = row[row.keys()[i]]
                orig_sd = sd_df[row.keys()
                                [i]]  # original std dev for current column
                orig_mean = means_df[row.keys()
                                     [i]]  # original mean for current column
                v = val_needed_for_shift(column_data[col], target_mean,
                                         orig_sd, orig_mean)
                new_obs_list.append(v)
                i += 1
            # Add new points to df
            new_row = local_df.mean(
            )  # unaffected features will gain a mean point
            new_row[feature_indexes] = new_obs_list
            local_df = local_df.append(new_row, ignore_index=True)
        if self.initialized:
            self.df = local_df
        return local_df

    def add_anomalies(self, anomalies_df, df=None):
        """
        Adds anomalous points to dataframe

        Args:
        df: DataFrame
            Data with features as columns and rows as observations.

        anomalies_df: DataFrame
            Column names (as ints) correspond to feature indexes in df.
            Rows contain series of magnitudes as multiples of standard deviation.

            The standard deviation is calculated on the original df before the points
            are added (not recalculated after each point). This is done so that the
            size of anomalous points can easily be compared at function call. The
            standard deviation will only be recalculated on function call.

            Unaffected features gain 1 observation equal to the mean.
            i.e.
            ---------
            |  1  | 3 |
            |---------|
            | -4  | 3 |
            | -6  | 4 |
            |  6  | 5 |
            ---------
            This data frame results in feature 1 gaining 3 points: one -4*sd away from
            the mean, one -6*sd away from the mean, and one 6*sd away from the mean.
            Feature 3 gains 3 points: one 3*sd away from the mean, one 4*sd away from
            the mean, and one 5*sd away from the mean.
            All other features gain 1 observation equal to the mean.
        """
        df = self._check_initialized(df)

        local_df = df.copy(deep=True)
        feature_indexes = anomalies_df.columns.values

        n_observations = local_df.shape[0]

        # iterate over rows of shift_df
        for index, row in anomalies_df.iterrows():
            # Add new points to df
            new_row = local_df.mean(
            )  # unaffected features will gain a mean point
            new_row[feature_indexes] = local_df[feature_indexes].std() * row
            local_df = local_df.append(new_row, ignore_index=True)

        if self.initialized:
            self.df = local_df
        return local_df

    def add_gaussian_observations(self, summary_df, feature_index, df=None, visualize=False):
        """
        Args:
        summary_df:
            Contains mean and standard deviation of gaussian distribution being added to
            a feature.
            In practice, means should be calculated as a ratio of the standard deviation
            before being passed to this method.
            i.e.
            ----------------------
            |  mean |  sd  | n_obs |
            |--------------|-------|
            |  2.3  |  1.2 |   10  |
            |   0   |  1.3 |   20  |
            ----------------------
        """
        df = self._check_initialized(df)

        local_df = df.copy(deep=True)
        new_data = None
        for index, row in summary_df.iterrows(
        ):  # iterate over rows of summary_df
            mean = row['mean']
            sd = row['sd']
            n = int(row['n_obs'])
            d = np.random.normal(mean, sd, n)
            if new_data is None:
                new_data = d
            else:
                new_data = np.concatenate((new_data, d))

        # Add new points to df by overwriting
        total_n_obs = summary_df['n_obs'].sum()
        local_df.loc[len(local_df) - total_n_obs:, feature_index] = new_data

        if visualize:
            import pyplot_themes as themes
            import seaborn as sns
            from matplotlib.pyplot import show
            themes.theme_ggplot2()
            # fig = plt.figure(figsize=(15,5))
            normal_color = 'royalblue'
            anomalous_color = 'orangered'
            added_idx = len(df)-total_n_obs
            p = sns.lineplot(data=local_df[feature_index][:(added_idx+1)], color=normal_color)
            sns.lineplot(data=local_df[feature_index][added_idx :], ax=p, color=anomalous_color) # plot added obs
            sns.scatterplot(data=local_df[feature_index][added_idx : ], ax=p, color='black') # add dots to all new data
            p.set_xlabel('Observation')
            p.set_ylabel(f'Feature {feature_index}')
            p.set_title(f'Feature {feature_index} with Added Observations')
            # plt.savefig(data_dir+'step shift_plot1.png', dpi=300)
            show()

        if self.initialized:
            self.df = local_df
        return local_df

    def get_data(self):
        return self.df


# Exposed methods that can be used as functions if the user does not use a Simulation object
# Choosing n=-1 is flag value (IGNORE: since only generate_data uses n and generate_data will not be exposed as a
# function, only as a method)
add_gaussian_observations = Simulation(-1).add_gaussian_observations
