## Installation
To install all dependencies, in the main pr_app  folder run the command `sh installations.sh`

## Model Training
To download the training data, run the following commands:
`wget http://vault.sfu.ca/index.php/s/hbWKX0zXYD2QoSU/download`

The dataset for training the SemEval Bias model is not publically available, hence we cannot share it here. However, the dataset can be downloaded from the lonk given below after taking approval from the author.
`https://zenodo.org/record/1489920#.XLPFmqdKg5k`

To train the models, run the following command `sh model_train.sh`

## Data Collection
To fetch all the data, run the command `sh fetch_data.sh`

## Dashboard Data
To generate the data needed for the dashboard, run the command, `sh run_dashboard_scripts.sh`

## Dashboard
To view the dashboard, run the following commands.
`cd dashboard`
`npm install`
`npm start`
You should now be able to view the dashaboard on http://localhost:3000/.