This dataset is based on the original available at https://www.kaggle.com/jiashenliu/515k-hotel-reviews-data-in-europe

The following processing steps were performed:

* Remove all reviews with a Reviewer_Score between 4 and 8.
* Added new column Approves, computed as Reviewer_Score > 5
* Removed all columns except for Negative_Review, Positive_Review and Reviewer_Score.

