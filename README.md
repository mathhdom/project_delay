# Probability of Delay in Reinforcement and Improvement Projects in the Brazilian Electrical Transmission System

![image](https://github.com/user-attachments/assets/38376061-a93d-4f97-a221-a7d9fd822853)

The objective of the project is to calculate the probability of delay in substation and transmission line projects.

#📝 Description

The first step was to obtain data from the Brazilian Electrical Agency through a Power BI report and ingest it into a raw database.

- link: https://portalrelatorios.aneel.gov.br/trans/trans

Secondly, an ETL process was necessary to extract only useful data for insertion into standard tables in a new database.

The next step was to create some features and consolidate all necessary data into an Analytical Base Table. After that, it was necessary to split it into two tables:

- Train table: Only data from completed projects;
- Prediction table: Only data from projects in planning or ongoing.

With the train table, it was possible to train the Random Forest Classifier Model and use MLFlow to manage the model.

After that, the model was able to predict the probability of delay for the prediction table data.

Finally, the data from the prediction was consumed by a Power BI report.

With the Power BI report, decision-makers can use it to analyze delay risks, prioritize projects, and set action plans. 

#🛠️ Technologies Used

- Python
- Pandas
- NumPy
- SQLAlchemy
- Scikit-learn
- MLFlow
- Pipeline (Scikit-learn)
- SQLite3
- Power BI

#📊 Results

The probability of delay from historical data, without any model, is around 61.25%. Therefore, any model that surpasses this target will be better than nothing.

When evaluating the model metrics, we have:

- Train Accuracy: 0.825
- Train Precision: 0.800
- Train Recall: 0.951
- Train Roc Auc: 0.925    

- Test Accuracy: 0.826
- Test Precision: 0.798
- Test Recall: 0.957
- Test Roc Auc: 0.916

#💡 Conclusion

Looking at the current accuracy compared to the historical probability, we can conclude that the model performs better than it.

Decision-makers can use this model to prioritize projects and manage the risks of delay, utilizing a friendly and dynamic report in Power BI.

For the next steps, it's possible to evaluate the current features and try to find new data to explore more important features.
