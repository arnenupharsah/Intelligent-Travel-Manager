# Intelligent-Travel-Manager

YFCC100M dataset
 * ```Melbourne-bigbox.csv```   Photos/videos taken inside of the big bounding box, output of ```src/filtering_bigbox.py```
 * ```trajectory_photos.csv```  Trajectorie file, output of ```src/generate_tables.py```
  * Each line represents one photo/video with following information
  * Trajectory_ID: trajectory ID of entry (multiple entries consist single trajectory)
  * Photo_ID: Unique Photo(Video) ID of entry
  * User_ID: User ID
  * Timestamp: When a photo/video has been taken
  * Longitude: Longitude of entry
  * Latitude: Latitude of entry
  * Accuracy: GPS Accuracy level (16 - the most accurate, 1 - the least accurate)
  * Marker: 0 if the entry is photo, 1 if the entry is video
  * URL: flickr URL to the entry
 * ```trajectory_stats.csv```  Stats for each trajectory, output of ```src/generate_tables.py```
  * Each line shows statistics about corresponding trajectory
  * Trajectory_ID: Unique trajectory ID
  * User_ID: User ID
  * #Photo: Number of photos+videos in the trajectory
  * Start_Time: When the first photo/video has been taken
  * Travel_Distance(km): Sum of the distances between consecutive points (Euclidean Distance)
  * Total_Time(min): The time gap between the first photo and the last photo
  * Average_Speed(km/h): Travel_Distances(km)/Total_Time(h)



Steps to make this project work:

$ tar xvzf web.py-0.40.tar.gz<br>
$ cd web.py-0.40<br>
$ sudo python setup.py install<br>
cd intelligent-travel-manager/src/recommender<br>
python3 demo.py

Then visit: `http://0.0.0.8080`
