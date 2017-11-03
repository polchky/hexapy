from math import sqrt, pow, cos, acos, sin, asin, pi, copysign

from .base_calculator import BaseCalculator

class BlocCalculator(BaseCalculator):
	def __init__(self, config):
		super().__init__(config)

	def get_angles(self, fx, fy, fz, leg):
		try:
			gx = self.config["gx"][leg]
			gy = self.config["gy"][leg]
			gz = self.config["gz"][leg]
			go = self.config["go"][leg]
			c = self.config


			# coxa-related distances
			gf = sqrt(pow(gx - fx, 2) + pow(gy - fy, 2))
			hf = sqrt(pow(gf, 2) - pow(c["gh"], 2))
			jh = c["gh"] * hf / gf
			gj = sqrt(pow(c["gh"], 2) - pow(jh, 2))

			# coxa-related positions
			jx = gx + (fx - gx) / gf * gj
			jy = gy + (fy - gy) / gf * gj
			hx = jx + (jy - gy) / gj * jh
			hy = jy + (gx - jx) / gj * jh

			# coxa-related angles
			tmp = acos((hx - gx) / c["gh"])
			xhf = tmp + pi / 2 if hy > gy else -tmp + pi / 2
			tmp = (xhf - go)

			# final coxa servo angle
			coxa_angle = tmp % (2 * pi) if tmp > 0 else tmp % (-2 * pi)
			if(abs(coxa_angle) > pi):
				coxa_angle -= copysign(coxa_angle, 1) * 2 * pi

			# foreleg-related data (relative to coxa)
			fx = sqrt(pow(fx - hx, 2) + pow(fy - hy, 2))
			fy = fz - gz
			bf = sqrt(pow(fx - c["hbxy"], 2) + pow(fy - c["hbz"], 2))
			ebf = acos((c["be"] ** 2 + bf ** 2 - c["ef"] ** 2) / (2 * c["be"] * bf))
			xbf = -pi / 2 + asin((fx - c["hbxy"]) / bf)

			# final outer servo angle
			outer_angle = ebf + xbf

			ex = c["hbxy"] + cos(outer_angle) * c["be"]
			ey = c["hbz"] + sin(outer_angle) * c["be"]
			dx = ex - (fx - ex) / c["ef"] * c["de"]
			dy = ey - (fy  - ey) / c["ef"] * c["de"]
			ad = sqrt(pow(dx - c["haxy"], 2) + pow(dy - c["haz"], 2))
			xad = asin((dy - c["haz"]) / ad)
			cad = acos((c["ac"] ** 2 + ad ** 2 - c["cd"] ** 2) / (2 * c["ac"] * ad))

			# final inner servo angle
			inner_angle = xad + cad

			return coxa_angle, outer_angle, inner_angle

		# invalid values for atirhmetic operations
		except ValueError:
			print("invalid input values")
			return False
