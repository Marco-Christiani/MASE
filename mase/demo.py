from mase.DataSimulation import *


def basic_demo():
    cov = np.eye(5)  # 5 independent features all with 0 mean
    sim = Simulation(100, covariance_matrix=cov)  # 100 observations
    summary_df = pd.DataFrame()
    summary_df['mean'] = [3, 0]
    summary_df['sd'] = [1, 1]
    summary_df['n_obs'] = [20, 10]
    feature_index = 0
    d = sim.get_data()
    print(d)
    sim.add_gaussian_observations(summary_df, feature_index, visualize=True)


def adding_obs_demo():
    """
    Demonstrate adding observations to existing data
    """
    cov = np.eye(5)  # 5 independent features all with 0 mean
    sim = Simulation(100, covariance_matrix=cov)  # 100 observations
    summary_df = pd.DataFrame()
    summary_df['mean'] = [3, 0]
    summary_df['sd'] = [1, 1]
    summary_df['n_obs'] = [20, 10]
    feature_index = 0
    d = sim.get_data()
    sim.add_gaussian_observations(summary_df, feature_index, visualize=False)

    # Add obs to existing df
    add_gaussian_observations(summary_df, feature_index, df=d, visualize=True, append=True)


if __name__ == '__main__':
    basic_demo()
    adding_obs_demo()
