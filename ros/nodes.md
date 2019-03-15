
# ROS

### Publisher

<details><summary>Python</summary>
<p>

```python
import rospy
from std_msgs.msg import String

pub = rospy.Publisher('chatter', String, queue_size=10)
rospy.init_node('talker', anonymous=True)
while not rospy.is_shutdown():
    hello_str = "hello world %s" % rospy.get_time()
    rospy.loginfo(hello_str)
    pub.publish(hello_str)
    rate.sleep()
```

</p>
</details>


<details><summary>C++</summary>
<p>

```cpp
#include "ros/ros.h"
#include "std_msgs/String.h"

ros::init(argc, argv, "talker");
ros::NodeHandle nh;
ros::Publisher chatter_pub = nh.advertise<std_msgs::String>("chatter", 1000);
ros::Rate loop_rate(10);
while (ros::ok()) {
    std_msgs::String msg;
    msg.data = "Hello World";
    chatter_pub.publish(msg);

    ros::spinOnce();
    loop_rate.sleep();
}
```

</p>
</details>

### Subscriber

<details><summary>Python</summary>
<p>

```python
import rospy
from std_msgs.msg import String

rospy.init_node('listener', anonymous=True)
rospy.Subscriber("chatter", String, callback)
rospy.spin()
```

</p>
</details>
<details><summary>C++</summary>
<p>

```cpp
#include "ros/ros.h"
#include "std_msgs/String.h"

void chatterCallback(const std_msgs::String::ConstPtr& msg) {
  ROS_INFO("I heard: [%s]", msg->data.c_str());
}

ros::init(argc, argv, "listener");
ros::NodeHandle nh;
ros::Subscriber sub = nh.subscribe("chatter", 1000, chatterCallback);
ros::spin();
```

</p>
</details>

### Service

<details><summary>Python</summary>
<p>

```python
import rospy
from std_srvs.srv import SetBool


def handle_service_rquest(req):
    return SetBoolResponse(success=True, message="")


rospy.init_node('node_name')
s = rospy.Service('set_bool', SetBool, handle_service_rquest)
rospy.spin()
```

</p>
</details>

### Service Client

<details><summary>Python</summary>
<p>

```python
import rospy
from std_srvs.srv import SetBool

def set_bool(data)
    rospy.wait_for_service('set_bool')
    try:
        set_bool_client = rospy.ServiceProxy('set_bool', SetBool)
        response = set_bool_client(data)
        return response.success
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
```

</p>
</details>

### Source
[ROS Python Documentation](http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29)