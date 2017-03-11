import smbus

from data_fetch import getData, RCP_OK, RCP_FAIL

bus = smbus.SMBus(1) # User SMBus(0) for version 1

# The address we setup in the Arduino Program
address = 0x25

LCDOK = 1
LCDFAIL = 0
GPSOK = 1
GPSFAIL = 0

def lcdplot(lcd_controller, data, ardu_status, gps_status):
  if ardu_status == RCP_OK:
    ardu_plot_status = "*"
  else:
    ardu_plot_status = "_"

  if gps_status == GPSOK:
    gps_plot_status = "*"
  else:
    gps_plot_status = "_"

  lcd_controller.plot(
    "Wspd: %03d A%s" % (data[1],ardu_plot_status),
    "Wdir: %03d G%s" % (data[0],gps_plot_status)
  )

def compute_wind_speed(wind_apparent_speed, wind_apparent_dir, fix_speed):
  """
    wind_apparent_speed in knots
    wind_apparent_dir in degrees wrt my direction
    fix_speed in m/s given by the gps
  """
  a = wind_apparent_speed
  b = fix_speed * 1.94
  th = wind_apparent_dir
  # law of cosine
  spd = math.sqrt(a * a + b * b - 2 * a * b * math.cos(math.pi * th / 180))
  return spd
