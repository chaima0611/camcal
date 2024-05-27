
def parse_args(x, y, theta):
        x_index = sys.argv.index('--x') if '--x' in sys.argv else None
        y_index = sys.argv.index('--y') if '--y' in sys.argv else None
        theta_index = sys.argv.index('--theta') if '--theta' in sys.argv else None
        
        x_command = float(sys.argv[x_index + 1]) if x_index is not None and x_index < len(sys.argv) else x
        y_command = float(sys.argv[y_index + 1]) if y_index is not None and y_index < len(sys.argv) else y
        theta_command = float(sys.argv[theta_index + 1]) if theta_index is not None and theta_index < len(sys.argv) else theta
        return x_command, y_command, theta_command


if __name__ == "__main__":
    bot = Rosmaster()
    bot.create_receive_threading()
    try:
        x, y, theta = initial_position()
        print("initial position: ", x, y, theta)
        target_x, target_y, target_theta = parse_args(x, y, theta)
        # target_theta = target_theta * 1000 * 3.14 / 180

        x_list, y_list, theta_list, vel_m1_list, vel_m2_list, vel_m3_list, vel_m4_list  = ctrl_robot_position(bot, target_x, target_y, target_theta, x, y, theta)

    except Exception:
        # Clear the cache data automatically sent by the MCU
        bot.clear_auto_report_data()

        # Restoring factory Settings
        bot.reset_flash_value()

        del bot
