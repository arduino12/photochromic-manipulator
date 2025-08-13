from pm import PM
from math import sqrt


def test_led_d_round_trip(pm, points):
    """
    test kinematics of offsetting the location of the led is correct by checking inversion property.
    """
    errs = []
    for (lx, ly) in points:
        print('original led point: ',lx,ly)
        dx, dy = pm.get_eo_location_from_led(lx, ly)
        print('d point: ',dx,dy)
        lx2, ly2 = pm.get_led_location_from_eo(dx, dy)
        print('reflexivity test led point: ',lx2,ly2)
        err = sqrt((lx2 - lx)**2 + (ly2 - ly)**2)
        print('error: ',err)
        errs.append(err)
    return max(errs), sum(errs)/len(errs)

def main():
    pm = PM(move_home=False)
    pts = [( -20, 30), ( 20, 30), ( 20, 50), ( -20, 50), ( -20, 30)]
    max_err, mean_err = test_led_d_round_trip(pm, pts)
    print(f"max_err={max_err:.4f}, mean_err={mean_err:.4f}")

if __name__ == '__main__':
    main()