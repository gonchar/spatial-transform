import glm
import unittest
from utils import *
from SpatialTransform import Transform, Euler

class Convertions(unittest.TestCase):
    def test_pointToWorld(self):
        for _ in range(randomSamples):
            p = randomPosition() * 10
            t = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            c = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            t.attach(c)
            self.assertEqual(c.pointToWorld(p), (t.Space * c.Space) * p)

    def test_pointTo(self):
        for _ in range(randomSamples):
            p = randomPosition() * 10
            t = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            c = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            t.attach(c)
            self.assertEqual(c.pointTo(p), glm.inverse(t.Space * c.Space) * p)

    def test_directionToWorld(self):
        for _ in range(randomSamples):
            p = randomPosition()
            t = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            c = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            t.attach(c)
            self.assertEqual(c.directionToWorld(p), (t.Rotation * c.Rotation) * p)

    def test_directionTo(self):
        for _ in range(randomSamples):
            p = randomPosition()
            t = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            c = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            t.attach(c)
            self.assertEqual(c.directionTo(p), glm.inverse((t.Rotation * c.Rotation)) * p)

class Rotations(unittest.TestCase):
    def test_setEuler(self):
        t = Transform()
        t.setEuler((+90, 0, 0), order='ZXY', extrinsic=True)
        self.assertGreater(deltaPosition, glm.distance(glm.vec3(0,+1,0), t.Forward))
        t.setEuler((-90, 0, 0), order='ZXY', extrinsic=True)
        self.assertGreater(deltaPosition, glm.distance(glm.vec3(0,-1,0), t.Forward))

        t.setEuler((0, +90, 0), order='ZXY', extrinsic=True)
        self.assertGreater(deltaPosition, glm.distance(glm.vec3(-1,0,0), t.Forward))
        t.setEuler((0, -90, 0), order='ZXY', extrinsic=True)
        self.assertGreater(deltaPosition, glm.distance(glm.vec3(+1,0,0), t.Forward))

        t.setEuler((0, 0, -90), order='ZXY', extrinsic=True)
        self.assertGreater(deltaPosition, glm.distance(glm.vec3(0,0,-1), t.Forward))
        t.setEuler((0, 0, +90), order='ZXY', extrinsic=True)
        self.assertGreater(deltaPosition, glm.distance(glm.vec3(0,0,-1), t.Forward))

        for _ in range(randomSamples):
            r = randomRotation()
            e = glm.degrees(glm.eulerAngles(r))
            t.setEuler(e, order='XYZ', extrinsic=True)
            angle = glm.angle(r * glm.inverse(t.Rotation))
            self.assertFalse(0.01 < angle < (glm.two_pi()-0.01))

    def test_lookAtWorld(self):
        for _ in range(randomSamples):
            t = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            c = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            t.attach(c)
            d = randomDirection()
            c.lookAtWorld(d)
            self.assertGreater(deltaPosition, glm.distance(glm.normalize(d), c.ForwardWorld))
            self.assertGreater(deltaPosition, glm.distance(t.RotationWorldInverse * glm.normalize(d), c.Forward))

    def test_lookAt(self):
        for _ in range(randomSamples):
            t = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            c = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            t.attach(c)
            d = randomDirection()
            c.lookAt(d)
            self.assertGreater(deltaPosition, glm.distance(glm.normalize(d), c.Forward))
            self.assertGreater(deltaPosition, glm.distance(t.RotationWorld * glm.normalize(d), c.ForwardWorld))

    def test_applyPosition(self):
        for _ in range(randomSamples):
            t = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            c = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            t.attach(c)
            childWorld = c.PositionWorld
            t.applyPosition()
            self.assertGreater(deltaPosition, glm.distance2(glm.vec3(0), t.Position))
            self.assertGreater(deltaPosition, glm.distance2(childWorld, c.PositionWorld))

            addition = randomPosition()
            t = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            c = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            t.attach(c)
            parent = t.Position
            childWorld = c.PositionWorld
            t.applyPosition(addition)
            self.assertGreater(deltaPosition, glm.distance2(parent + addition, t.Position))
            self.assertGreater(deltaPosition, glm.distance2(childWorld, c.PositionWorld))

    def test_applyRotation(self):
        for _ in range(randomSamples):
            t = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            c = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            t.attach(c)
            childWorld = c.RotationWorld
            t.applyRotation()
            self.assertGreater(deltaRotation, glm.angle(t.Rotation))
            self.assertGreater(deltaRotation, glm.angle(glm.inverse(c.RotationWorld) * childWorld))

            addition = randomRotation()
            t = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            c = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            t.attach(c)
            parent = t.Rotation
            childWorld = c.RotationWorld
            t.applyRotation(addition)
            self.assertGreater(deltaRotation, glm.angle((parent * addition) * glm.inverse(t.Rotation)))
            self.assertGreater(deltaRotation, glm.angle(childWorld * glm.inverse(c.RotationWorld)))

    def test_applyScale(self):
        for _ in range(randomSamples):
            t = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            c = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            t.attach(c)
            childWorld = c.ScaleWorld
            t.appyScale()
            self.assertGreater(deltaPosition, glm.distance2(glm.vec3(1), t.Scale))
            self.assertGreater(deltaPosition, glm.distance2(childWorld, c.ScaleWorld))

            addition = randomScale()
            t = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            c = Transform(position=randomPosition(), rotation=randomRotation(), scale=randomScale())
            t.attach(c)
            parent = t.Scale
            childWorld = c.ScaleWorld
            t.appyScale(addition)
            self.assertGreater(deltaPosition, glm.distance2(parent * addition, t.Scale))
            self.assertGreater(deltaPosition, glm.distance2(childWorld, c.ScaleWorld))

if __name__ == '__main__':
    unittest.main()
