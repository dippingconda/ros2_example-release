import rclpy
from morai_msgs.srv import MoraiEventCmdSrv
from rclpy import node

def main(args=None):
  rclpy.init(args=args)

  node = rclpy.create_node('MoraiEventCmdSrv')
  client = node.create_client(MoraiEventCmdSrv, 'morai_msgs/MoraiEventCmdSrv')

  srv_def = MoraiEventCmdSrv.Request()
  srv_def.request.option = 1
  srv_def.request.ctrl_mode = 4
  srv_def.request.gear = 3
  srv_def.request.lamps.turn_signal = 1
  srv_def.request.lamps.emergency_signal = 1
  srv_def.request.set_pause = False

  while not client.wait_for_service(timeout_sec=10.0):
    node.get_logger().info('service not available, waiting again...')
  
  node.get_logger().info(f'{srv_def}')
  future = client.call_async(srv_def)
  while rclpy.ok():
    rclpy.spin_once(node)
    if future.done():
      try:
        result = future.result()
      except Exception as e:
        node.get_logger().info('Service call failed %r' %(e,))
      else:
        node.get_logger().info(
          f'Result of MoraiEventCmdSrv : {result}')
      
      break
  node.destroy_node()
  rclpy.shutdown()

if __name__ == '__main__':
  main()
