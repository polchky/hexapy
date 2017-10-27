from math import sqrt, pow, cos, acos, sin, asin, pi, copysign

class BaseCalculator:
	def __init__(self, config):
		self.config = config




class ThreeCoxa(BaseCalculator):
	def __init__(self, config):
		BaseCalculator.__init__(self, config)

	def getangles(self, fx, fy, fz, leg):
		try:
			gx = self.config["gx"][leg]
			gy = self.config["gy"][leg]
			gz = self.config["gz"][leg]
			go = self.config["go"][leg]
			c = self.config


			# compute coxa-related distances
			gf = sqrt(pow(gx - fx, 2) + pow(gy - fy, 2))
			hf = sqrt(pow(gf, 2) - pow(c["gh"], 2))
			jh = c["gh"] * hf / gf
			gj = sqrt(pow(c["gh"], 2) - pow(jh, 2))

			# compute coxa-related positions
			jx = gx + (fx - gx) / gf * gj
			jy = gy + (fy - gy) / gf * gj
			hx = jx + (jy - gy) / gj * jh
			hy = jy + (gx - jx) / gj * jh

			# compute coxa-related angles
			tmp = acos((hx - gx) / c["gh"])
			xhf = tmp + pi / 2 if hy > gy else -tmp + pi / 2
			tmp = (xhf - go)

			# final coxa servo angle
			coxaangle = tmp % (2 * pi) if tmp > 0 else tmp % (-2 * pi)
			if(abs(coxaangle) > pi):
				coxaangle -= copysign(coxaangle, 1) * 2 * pi

			# compute foreleg-related data (relative to coxa)
			fx = sqrt(pow(fx - hx, 2) + pow(fy - hy, 2))
			fy = fz - gz
			bf = sqrt(pow(fx - c["hbxy"], 2) + pow(fy - c["hbz"], 2))
			ebf = acos((c["be"] ** 2 + bf ** 2 - c["ef"] ** 2) / (2 * c["be"] * bf))
			xbf = -pi / 2 + asin((fx - c["hbxy"]) / bf)

			# final outer servo angle
			outerangle = ebf + xbf
			ex = c["hbxy"] + cos(outerangle) * c["be"]
			ey = c["hbz"] + sin(outerangle) * c["be"]
			dx = ex - (fx - ex) / c["ef"] * c["de"]
			dy = ey - (fy  - ey) / c["ef"] * c["de"]
			ad = sqrt(pow(dx - c["haxy"], 2) + pow(dy - c["haz"], 2))
			xad = asin((dy - c["haz"]) / ad)
			cad = acos((c["ac"] ** 2 + ad ** 2 - c["cd"] ** 2) / (2 * c["ac"] * ad))

			# final inner servo angle
			innerangle = xad + cad

			return coxaangle, outerangle, innerangle
		except ValueError:
			print("invalid input arguments")
			return False


config = {"gx": [49.85], "gy": [84.85], "gz": [0], "go": [0.79], "gh": 19.2, "haxy": -12, "haz": 14, "hbxy": 12, "hbz": 14, "ac": 55, "cd": 50, "be": 40, "de": 40, "ef": 90}

calc = ThreeCoxa(config)

print(calc.getangles(46.14, 142.73, -70, 0))
