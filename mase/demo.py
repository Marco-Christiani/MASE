import matplotlib.pyplot as plt
import pyplot_themes as themes
import seaborn as sns
from mase.DataSimulation import *


def run_demo():
    # demo1()

    # Generate data with matching mean and correlation structure provided
    # means = summary_df[['mean']].to_numpy()
    # means = means.reshape(1, -1)[0]
    #
    # sim_data = generate_data(np.zeros(56), 200)
    # sim_df = pd.DataFrame(sim_data)

    # anomaly_demo()
    # new_df = demo_step_shift()
    # new_df = demo_smooth_shift(new_df)
    # new_df.to_csv(data_dir+'sim_data_1smooth_1step.csv', index=False)
    cov = np.eye(5)  # 5 independent features all with 0 mean
    sim = Simulation(100, covariance_matrix=cov)  # 100 observations
    summary_df = pd.DataFrame()
    summary_df['mean'] = [3, 0]
    summary_df['sd'] = [1, 1]
    summary_df['n_obs'] = [20,10]
    feature_index = 0
    sim.add_gaussian_observations(summary_df, feature_index)
    d = sim.get_data()
    print(d)
    sim.add_gaussian_observations(summary_df, feature_index, visualize=True)

def demo1():
    # Generate data with matching mean and correlation structure provided
    means = summary_df[['mean']].to_numpy()
    means = means.reshape(1, -1)[0]

    sim_data = generate_data(np.zeros(56), 100)
    sim_df = pd.DataFrame(sim_data)

    # Demonstrate mean drift
    # Feature 2 will undergo a smooth mean drift from 0.1sd to 1sd in 10 observations
    feature2_drift = list(np.linspace(0,1,num=20)) # 10 obs evenly spaced on []
    # Feature 6 will undergo a custom mean drift from 0.1 to 1 in 10 observations
    # feature6_drift = [0.1, 0.15, 0.15, 0.21, 0.3, 0.45, 0.65, 0.7, 0.5, 1]
    feature6_drift =feature2_drift

    shifts_df = pd.DataFrame(columns=[2,6])
    shifts_df[2] = feature2_drift
    shifts_df[6] = feature6_drift
    drifted_df = add_mean_drift(sim_df, shifts_df)
    print(f'Means before drift:\n{sim_df.mean()[[2,6]]}\n')
    print(f'Means after drift:\n{drifted_df.mean()[[2,6]]}\n')

    # Generate Plots to Demonstrate Effects
    sns.set()
    plt.rcParams['lines.linewidth'] = 3
    title_fontsize = 15
    tick_size = 12
    ax_font = {'weight':'semibold', 'size': 14}
    fig = plt.figure(figsize=(16,16))
    # Check feature 2
    ax = sns.lineplot(data=sim_df[2], ax=fig.add_subplot(221))
    sns.lineplot(data=drifted_df[2][99:], ax=ax)
    sns.scatterplot(data=drifted_df[2][100:], ax=ax, color='red')
    # ax.set_ylim(-1,23)
    ax.set_xlabel('Observation')
    ax.set_ylabel('Feature 2')
    ax.set_title('Feature 2 Observations After Adding Mean Drift')
    # Check feature 6
    ax = sns.lineplot(data=sim_df[6], ax=fig.add_subplot(222))
    sns.lineplot(data=drifted_df[6][99:], ax=ax)
    sns.scatterplot(data=drifted_df[6][100:], ax=ax, color='red')
    # ax.set_ylim(-1,23)
    ax.set_xlabel('Observation')
    ax.set_ylabel('Feature 6')
    ax.set_title('Feature 6 Observations After Adding Mean Drift')

    # Check feature 2 rolling mean
    f2_rolling_mean = sim_df[2].expanding(min_periods=5).mean()
    f2_drifted_rolling_mean = drifted_df[2].expanding(min_periods=5).mean()

    ax = sns.lineplot(data=f2_rolling_mean, ax=fig.add_subplot(223))
    sns.lineplot(data=f2_drifted_rolling_mean[99:], ax=ax)
    sns.scatterplot(data=f2_drifted_rolling_mean[99:], ax=ax, color='red')
    # ax.set_ylim(-1.5,1.5)
    ax.set_xlabel('Observation')
    ax.set_ylabel('Feature 2')
    ax.set_title('Feature 2 Rolling Mean')
    # Check feature 6 rolling mean
    f6_rolling_mean = sim_df[6].expanding(min_periods=5).mean()
    f6_drifted_rolling_mean = drifted_df[6].expanding(min_periods=5).mean()

    ax = sns.lineplot(data=f6_rolling_mean, ax=fig.add_subplot(224))
    sns.lineplot(data=f6_drifted_rolling_mean[99:], ax=ax)
    sns.scatterplot(data=f6_drifted_rolling_mean[100:], ax=ax, color='red')
    # ax.set_ylim(-1.5,1.5)

    ax.set_xlabel('Observation')
    ax.set_ylabel('Feature 6')
    ax.set_title('Feature 6 Rolling Mean')
    plt.show()

def demo_step_shift():
    # Demonstrate adding gaussian observations
    sd = sim_df[3].std()
    mean = sim_df[3].mean()

    step_shift_mean = mean+2.5*sd
    step_shift_sd = sd

    feature3_means = [step_shift_mean, # mean for step shift data
                    mean] # return to "normal" mean
    feature3_sd = [step_shift_sd, # sd for step shift data
                sd] # return to "normal" sd
    # Overwrite last 50 observations with 30 anomalous and 20 "normal"
    n_anomalous = 30 # Generate 30 step shift observations
    n_normal = 20 # End with 20 "normal" observations
    n_total = n_anomalous+n_normal # total number of observations we are simulating/overwriting
    feature3_n_obs = [n_anomalous, n_normal]

    f3summary_df = pd.DataFrame()
    f3summary_df['mean'] = feature3_means
    f3summary_df['sd'] = feature3_sd
    f3summary_df['n_obs'] = feature3_n_obs
    new_df = add_gaussian_observations(sim_df, f3summary_df, 3)

    # Generate plots to demonstrate effects

    fig = plt.figure(figsize=(15,5))
    # Check feature 3
    normal_color = 'royalblue'
    anomalous_color = 'orangered'
    anomalous_idx = len(sim_df)-n_total
    normal_idx = len(sim_df)-n_normal
    p = sns.lineplot(data=new_df[3][:(anomalous_idx+1)], color=normal_color)
    sns.lineplot(data=new_df[3][anomalous_idx : normal_idx], ax=p, color=anomalous_color) # plot anomalies
    sns.lineplot(data=new_df[3][normal_idx-1: ], ax=p, color=normal_color) # plot "normal"
    sns.scatterplot(data=new_df[3][anomalous_idx : ], ax=p, color='black') # add dots to all new data
    p.set_xlabel('Observation')
    p.set_ylabel('Feature 3')
    p.set_title('Feature 3 with $\mu+2.5\sigma$ Step Shift')
    # plt.savefig(data_dir+'step shift_plot1.png', dpi=300)
    plt.show()

    # Check feature 3 rolling mean
    f3_rolling_mean = sim_df[3].expanding(min_periods=5).mean()
    f3_new_rolling_mean = new_df[3].expanding(min_periods=5).mean()

    p2 = sns.lineplot(data=f3_rolling_mean[:anomalous_idx])
    sns.lineplot(data=f3_new_rolling_mean[anomalous_idx:], ax=p2)
    # ax.set_ylim(-1.5,1.5)
    p2.set_xlabel('Observation')
    p2.set_ylabel('Feature 3')
    p2.set_title('Feature 3 Rolling Mean')
    plt.show()
    return new_df

def demo_smooth_shift(df):
    # Demonstrate adding gaussian observations
    sd = sim_df[5].std()
    mean = sim_df[5].mean()

    n_means = 10 # will use 10 subtle mean changes
    feature5_means = mean+sd*np.linspace(0, 2, n_means)
    feature5_sd = list(np.repeat(sd, n_means))
    # Overwrite last 50 observations with 30 anomalous and 20 "normal"
    obs_per_shift = 5 # 5 observations per intermediate means
    n_total = n_means*obs_per_shift # total number of observations we are simulating/overwriting
    feature3_n_obs = np.repeat(obs_per_shift, n_means)

    f5summary_df = pd.DataFrame()
    f5summary_df['mean'] = feature5_means
    f5summary_df['sd'] = feature5_sd
    f5summary_df['n_obs'] = obs_per_shift
    new_df = add_gaussian_observations(df, f5summary_df, 5)

    # Generate plots to demonstrate effects
    themes.theme_ggplot2()
    fig = plt.figure(figsize=(15,5))
    # Check feature 3
    normal_color = 'royalblue'
    anomalous_color = 'orangered'
    anomalous_idx = len(sim_df)-n_total
    p = sns.lineplot(data=new_df[5][:(anomalous_idx+1)], color=normal_color)
    sns.lineplot(data=new_df[5][anomalous_idx : ], ax=p, color=anomalous_color) # plot anomalies
    sns.scatterplot(data=new_df[5][anomalous_idx : ], ax=p, color='black') # add dots to all new data
    p.set_xlabel('Observation')
    p.set_ylabel('Feature 5')
    p.set_title('Feature 5 with $\mu+2\sigma$ Smooth Shift')
    # plt.savefig(data_dir+'step shift_plot1.png', dpi=300)
    plt.show()

    # Check feature 5 rolling mean
    f5_rolling_mean = sim_df[5].expanding(min_periods=5).mean()
    f5_new_rolling_mean = new_df[5].expanding(min_periods=5).mean()

    p2 = sns.lineplot(data=f5_rolling_mean[:anomalous_idx])
    sns.lineplot(data=f5_new_rolling_mean[anomalous_idx:], ax=p2)
    # ax.set_ylim(-1.5,1.5)
    p2.set_xlabel('Observation')
    p2.set_ylabel('Feature 5')
    p2.set_title('Feature 5 Rolling Mean')
    plt.show()
    return new_df


def anomaly_demo():
    # Demonstrate adding anomalies
    anomalies_df = pd.DataFrame([[-4,3],
                                 [-6,4],
                                 [6,5]], columns=[1,3] )
    anomalous_df = add_anomalies(sim_df, anomalies_df)

    # Generate plots to demonstrate effects
    fig = plt.figure(figsize=(16,8))
    # Check feature 1
    ax = sns.lineplot(data=sim_df[1], ax=fig.add_subplot(121))
    sns.lineplot(data=anomalous_df[1][99:], ax=ax)
    sns.scatterplot(data=anomalous_df[1][100:], ax=ax, color='red')
    ax.set_xlabel('Observation')
    ax.set_ylabel('Feature 1')
    ax.set_title('Feature 1 with Anomalies Added')
    # Check feature 3
    ax = sns.lineplot(data=sim_df[3], ax=fig.add_subplot(122))
    sns.lineplot(data=anomalous_df[3][99:], ax=ax)
    sns.scatterplot(data=anomalous_df[3][100:], ax=ax, color='red')
    ax.set_xlabel('Observation')
    ax.set_ylabel('Feature 3')
    ax.set_title('Feature 3 with Anomalies Added')
    plt.show()

if __name__ == '__main__':
    run_demos()

