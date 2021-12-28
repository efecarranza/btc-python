from __future__ import annotations
from dataclasses import dataclass

def extended_euclidean_algorithm(a, b):
	old_r, r = a, b
	old_s, s = 1, 0
	old_t, t = 0, 1
	while r != 0:
		quotient = old_r // r
		old_r, r = r, old_r - quotient * r
		old_s, s = s, old_s - quotient * s
		old_t, t = t, old_t - quotient * t
	return old_r, old_s, old_t

def inv(n, p):
	gcd, x, y = extended_euclidean_algorithm(n, p)
	return x % p

@dataclass
class Curve:
	p: int
	a: int
	b: int

@dataclass
class Point:
	curve: Curve
	x: int
	y: int

	def __add__(self, other: Point) -> Point:
		if self == INF:
			return other
		if other == INF:
			return self
		if self.x == other.x and self.y != other.y:
			return INF

		if self.x == other.x:
			m = (3 * self.x**2 + self.curve.a) * inv(2 * self.y, self.curve.p)
		else:
			m = (self.y - other.y) * inv(self.x - other.x, self.curve.p)

		rx = (m**2 - self.x - other.x) % self.curve.p
		ry = (-(m*(rx - self.x) + self.y)) % self.curve.p
		return Point(self.curve, rx, ry)

	def __rmul__(self, k: int) -> Point:
		assert isinstance(k, int) and k >= 0
		result = INF
		append = self
		while k:
			if k & 1:
				result += append
			append += append
			k >>= 1
		return result

@dataclass
class Generator:
	G: Point
	n: int

INF = Point(None, None, None)
