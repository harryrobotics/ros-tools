# rostools

##bag_to_csv_harry

Usage


`./bag_to_csv_harry.py bags_list` : to list all bag files in current folder

`./bag_to_csv_harry topics_list bagName` : to list all topics of a bag file
e.g bagName = ros_bag_file.bag
`./bag_to_csv_harry.py topics_list ./ros_bag_file.bag`

`./bag_to_csv_harry.py read bagName topics` : to convert specific topics to csv e.g: bag2csv.py read bagName /topic1 /topic2
