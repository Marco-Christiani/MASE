Adding to Existing Data
=======================

To add observations to existing data is simple, just load the existing data into a DataFrame and use the ``add_gaussian_observations()`` function. 

.. code-block:: python

	my_data = # load data
	specs_df = # define specs_df as before
	mase.add_gaussian_observations(specs_df, feature_index, df=my_data, append=True)


*Contrast this with creating a Simulation object and using the add_gaussian_observations() method*