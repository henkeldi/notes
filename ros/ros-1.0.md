
# ROS


<details><summary>C++</summary><blockquote><p>

<details><summary>Publisher</summary>

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

<details><summary>Subscriber</summary>

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

<details><summary>Service</summary>

```cpp
#include "ros/ros.h"
#include "std_srvs/SetBool.h"

bool set_bool(std_srvs::SetBool::Request  &req,
         std_srvs::SetBool::Response &res)
{
  // do something with req.data
  res.success = true;
  res.message = "OK";
  return true;
}

int main(int argc, char **argv) {
  ros::init(argc, argv, "add_two_ints_server");
  ros::NodeHandle n;

  ros::ServiceServer service = n.advertiseService("set_bool", set_bool);
  ros::spin();

  return 0;
}
```
</details>

<details><summary>Service Client</summary>

```C++
#include "ros/ros.h"
#include "beginner_tutorials/AddTwoInts.h"
#include <cstdlib>

int main(int argc, char **argv) {
  ros::NodeHandle n;
  ros::ServiceClient client = n.serviceClient<beginner_tutorials::AddTwoInts>("add_two_ints");
  beginner_tutorials::AddTwoInts srv;
  srv.request.a = atoll(argv[1]);
  srv.request.b = atoll(argv[2]);
  if (client.call(srv))
  {
    ROS_INFO("Sum: %ld", (long int)srv.response.sum);
  }
  else
  {
    ROS_ERROR("Failed to call service add_two_ints");
    return 1;
  }

  return 0;
}
```
</details>

</details>


<details><summary>Python</summary><blockquote><p>

<details><summary>Publisher</summary>

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

<details><summary>Subscriber</summary>

```python
import rospy
from std_msgs.msg import String

rospy.init_node('listener', anonymous=True)
rospy.Subscriber("chatter", String, callback)
rospy.spin()
```
</details>

<details><summary>Service</summary>

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

<details><summary>Service Client</summary>

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

</details>


<details><summary>Kotlin</summary><blockquote><p>

<details><summary>Publisher</summary>

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

<details><summary>Subscriber</summary>

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

<details><summary>Service</summary>
</details>

<details><summary>Service Client</summary>
</details>

</details>


<details><summary>Javascript</summary><blockquote><p>

<details><summary>Publisher</summary>

```javascript
let ros = new ROSLIB.Ros({
    url : 'ws://localhost:9090'
});

ros.on('connection', function() {
    console.log('Connected to websocket server.');
});

ros.on('error', function(error) {
    console.log('Error connecting to websocket server: ', error);
});

ros.on('close', function() {
    console.log('Connection to websocket server closed.');
});

const cmdVel = new ROSLIB.Topic({
    ros : ros,
    name : '/cmd_vel',
    messageType : 'geometry_msgs/Twist'
});

const twist = new ROSLIB.Message({
    linear : {
        x : 0.1,
        y : 0.2,
        z : 0.3
    },
    angular : {
        x : -0.1,
        y : -0.2,
        z : -0.3
    }
});
cmdVel.publish(twist);
```
</details>

<details><summary>Subscriber</summary>

```javascript
let ros = new ROSLIB.Ros({
    url : 'ws://localhost:9090'
});

ros.on('connection', function() {
    console.log('Connected to websocket server.');
});

ros.on('error', function(error) {
    console.log('Error connecting to websocket server: ', error);
});

ros.on('close', function() {
    console.log('Connection to websocket server closed.');
});

let listener = new ROSLIB.Topic({
    ros : ros,
    name : '/listener',
    messageType : 'std_msgs/String'
});

listener.subscribe(function(message) {
    console.log('Received message on ' + listener.name + ': ' + message.data);
    listener.unsubscribe();
});
```
</details>

<details><summary>Service Client</summary>

```javascript
let ros = new ROSLIB.Ros({
    url : 'ws://localhost:9090'
});

ros.on('connection', function() {
    console.log('Connected to websocket server.');
});

ros.on('error', function(error) {
    console.log('Error connecting to websocket server: ', error);
});

ros.on('close', function() {
    console.log('Connection to websocket server closed.');
});

let addTwoIntsClient = new ROSLIB.Service({
    ros : ros,
    name : '/add_two_ints',
    serviceType : 'rospy_tutorials/AddTwoInts'
});

let request = new ROSLIB.ServiceRequest({
    a : 1,
    b : 2
});

addTwoIntsClient.callService(request, result => {
    console.log('Result for service call on '
      + addTwoIntsClient.name
      + ': '
      + result.sum);
});
```
</details>

</details>

## Compile on Raspbian

```bash
mkdir -p ~/ros_catkin_ws
rosinstall_generator ros_comm actionlib actionlib_msgs \
    --rosdistro melodic --deps --wet-only --tar\
    > melodic-ros_comm-wet.rosinstall
wstool init -j8 src melodic-ros_comm-wet.rosinstall
rosdep install --from-paths src --ignore-src --rosdistro melodic -y
sudo mkdir -p /opt/ros/melodic
sudo chown pi:pi /opt/ros/melodic
./src/catkin/bin/catkin_make_isolated -j2 --install\
    --install-space /opt/ros/melodic -DCMAKE_BUILD_TYPE=Release
```

### Source
[ROS Python Documentation](http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29)