
# ROS

<details><summary>Publisher</summary><blockquote><p>

<details><summary>Python</summary>

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
</details>

<details><summary>C++</summary>

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
</details>

<details><summary>Kotlin</summary>

```kotlin
import org.ros.concurrent.CancellableLoop
import org.ros.namespace.GraphName
import org.ros.node.*
import java.net.URI

fun main(args: Array<String>) {
    val nodeConfig = NodeConfiguration.newPublic("127.0.0.1", URI.create("http://127.0.0.1:11311"))
    DefaultNodeMainExecutor.newDefault().execute(PublisherNode(), nodeConfig)
}

class PublisherNode: NodeMain {
    override fun getDefaultNodeName(): GraphName {return GraphName.of("PublisherNode")}
    override fun onShutdownComplete(node: Node?) {}
    override fun onShutdown(node: Node?) {}
    override fun onError(node: Node?, throwable: Throwable?) {}
    override fun onStart(connectedNode: ConnectedNode?) {
        val publisher = connectedNode?.newPublisher<std_msgs.String>("chatter",
            std_msgs.String._TYPE)

        connectedNode?.executeCancellableLoop(object: CancellableLoop() {
            override fun loop() {
                val str = publisher?.newMessage()
                str?.data = "Hallo"
                publisher?.publish(str)
                Thread.sleep(1000)
            }
        })
    }
}
```
</details>

</p></blockquote>
</details>


<details><summary>Subscriber</summary><blockquote><p>

<details><summary>Python</summary>


```python
import rospy
from std_msgs.msg import String

rospy.init_node('listener', anonymous=True)
rospy.Subscriber("chatter", String, callback)
rospy.spin()
```
</details>

<details><summary>C++</summary>

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
</details>

<details><summary>Kotlin</summary>

```kotlin
import org.ros.concurrent.CancellableLoop
import org.ros.namespace.GraphName
import org.ros.node.*
import java.net.URI

fun main(args: Array<String>) {
    val nodeConfig = NodeConfiguration.newPublic("127.0.0.1", URI.create("http://127.0.0.1:11311"))
    DefaultNodeMainExecutor.newDefault().execute(SubscriberNode(), nodeConfig)
}

class SubscriberNode: NodeMain {
    override fun getDefaultNodeName(): GraphName {return GraphName.of("SubscriberNode")}
    override fun onShutdownComplete(node: Node?) {}
    override fun onShutdown(node: Node?) {}
    override fun onError(node: Node?, throwable: Throwable?) {}
    override fun onStart(connectedNode: ConnectedNode?) {
        val subscriber = connectedNode?.newSubscriber<std_msgs.String>("chatter",
            std_msgs.String._TYPE)

        subscriber?.addMessageListener {
            println("I heard ${it.data}")
        }
    }
}
```
</details>

</p></blockquote>
</details>


<details><summary>Service</summary><p><blockquote>

<details><summary>Python</summary>


```python
import rospy
from std_srvs.srv import SetBool


def handle_service_rquest(req):
    return SetBoolResponse(success=True, message="")


rospy.init_node('node_name')
s = rospy.Service('set_bool', SetBool, handle_service_rquest)
rospy.spin()
```

</details>

</p></blockquote>
</details>


<details><summary>Service Client</summary><p><blockquote>

<details><summary>Python</summary>

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

</details>

</p></blockquote>
</details>


### Source
[ROS Python Documentation](http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29)