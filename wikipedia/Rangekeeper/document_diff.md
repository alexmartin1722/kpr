# Document diff — Rangekeeper
*Sentence-level diff, original English → after the KPR merge. 82 lines added/changed.*

```diff
--- Rangekeeper (original English)
+++ Rangekeeper (after KPR merge)
@@ -15,2 +15,3 @@
 It also requires accurately knowing the own ship's course and speed.
+The direction indicated by a gyrocompass is independent of the ship's course.
 Target position prediction When a gun is fired, it takes time for the projectile to arrive at the target.
@@ -18,4 +19,7 @@
 This is the point at which the guns are aimed.
+The plotting table predicts the position of the artillery platform.
 Gunfire correction Directing the fire of a long-range weapon to deliver a projectile to a specific location requires many calculations.
 The projectile point of impact is a function of many variables, including: gun azimuth, gun elevation, wind speed and direction, air resistance, gravity, latitude, gun/sight parallax, barrel wear, powder load, and projectile type.
+Observation equipment includes a PCKA on the gun.
+The shell clock determines the time from firing to the shell's impact.
 
@@ -24,7 +28,11 @@
 Even during the American Civil War, the famous engagement between the and the was often conducted at less than range.
+Fire control required observers to see the target directly.
 With time, naval guns became larger and had greater range.
+There was an urgent need for accurate long-range shooting.
 At first, the guns were aimed using the technique of artillery spotting.
 Artillery spotting involved firing a gun at the target, observing the projectile's point of impact (fall of shot), and correcting the aim based on where the shell was observed to land, which became more and more difficult as the range of the gun increased.
+The experience proved that a fire-control director must be installed on all ships.
 
 Between the American Civil War and 1905, numerous small improvements were made in fire control, such as telescopic sights and optical rangefinders.
+A rangefinder can be a non-optical device.
 There were also procedural improvements, like the use of plotting boards to manually predict the position of a ship during an engagement.
@@ -32,3 +40,5 @@
 These devices were early forms of rangekeepers.
-
+The idea of such a mechanism was first proposed by Leibniz.
+Hannibal Ford created mechanical analog computers.
+William Newell created mechanical analog computers.
 The issue of directing long-range gunfire came into sharp focus during World War I with the Battle of Jutland.
@@ -39,3 +49,5 @@
 
-The US Navy's first deployment of a rangekeeper was on the in 1916.
+The US Navy's first deployment of a rangekeeper was on the USS Texas (BB-35) in 1916.
+The SRP was first implemented in the US Navy in 1916.
+The Texas was the first US Navy ship to use fire control systems.
 Because of the limitations of the technology at that time, the initial rangekeepers were crude.
@@ -56,5 +68,7 @@
 The term "computer," which had been reserved for human calculators, came to be applied to the rangekeeper equipment.
+The increase in capabilities was so significant that the name 'computing device' no longer fit reality.
+The Torpedo Data Computer was first adopted in the 1940s.
 After World War II, digital computers began to replace rangekeepers.
+After the war, digital computers began to replace calculating and decision-making devices.
 However, components of the analog rangekeeper system continued in service with the US Navy until the 1990s.
-
 The performance of these analog computers was impressive.
@@ -62,4 +76,5 @@
 It is a major advantage for a warship to be able to maneuver while engaging a target.
-
 Night naval engagements at long range became feasible when radar data could be input to the rangekeeper.
+Accuracy increased with the use of radar data.
+Accuracy increased during night battles.
 The effectiveness of this combination was demonstrated in November 1942 at the Third Battle of Savo Island when the engaged the Japanese battlecruiser at a range of at night.
@@ -70,3 +85,2 @@
 The Royal Navy began to introduce gyroscopic stabilization of their director gunsights in World War One and by the start of World War Two all warships fitted with director control had gyroscopically controlled gunsights.
-
 The last combat action for the analog rangekeepers, at least for the US Navy, was in the 1991 Persian Gulf War when the rangekeepers on the s directed their last rounds in combat.
@@ -74,5 +88,5 @@
 Rangekeepers were very large, and the ship designs needed to make provisions to accommodate them.
-For example, the Ford Mk 1A Computer weighed The Mk.
+For example, the Ford Mk 1A Computer weighed 1430 kg, and the Mk.
 1/1A's mechanism support plates, some were up to thick, were made of aluminum alloy, but nevertheless, the computer is very heavy.
-On at least one refloated museum ship, the destroyer (now in Boston), the computer and Stable Element more than likely still are below decks, because they are so difficult to remove.
+On at least one refloated museum ship, the destroyer (now in Boston), the computer and Stable Element more than likely still are below decks, because they are so difficult to remove, and the LVPs and stabilizing elements can still be seen on the museum ship USS Cassin Young.
 
@@ -96,4 +110,4 @@
 Shell-to-shell repeatability was ≈0.4% of range.
-
 Accurate long-range gunnery requires that a number of factors be taken into account: Target course and speed Own ship course and speed Gravity Coriolis effect: Because the Earth is rotating, there is an apparent force acting on the projectile.
+The magnitude of the Coriolis effect depends on latitude.
 Internal ballistics: Guns do wear, and this aging must be taken into account by keeping an accurate count of the number of projectiles sent through the barrel (this count is reset to zero after the installation of a new liner).
@@ -102,2 +116,3 @@
 Also, air conditions have an effect as well (temperature, wind, air pressure).
+Air density affects the trajectory of the projectile.
 Parallax correction: In general, the position of the gun and target spotting equipment (radar, mounted on the gun director, pelorus, etc) are in different locations on a ship.
@@ -105,3 +120,9 @@
 Projectile characteristics (e.g. ballistic coefficient) Powder charge weight and temperature
-
+Ships move side to side.
+Ships move forward and backward.
+A ship rolls from side to side.
+A ship pitches from bow to stern.
+The firing ship performs evasion maneuvers against target fire.
+This effect causes the gun barrel of the firing ship to have certain traverse and elevation velocities.
+These velocities have a significant impact on the impact location of the shell.
 The calculations to predict and compensate for all these factors are complicated, frequent and error-prone when done by hand.
@@ -109,3 +130,2 @@
 For example, information from the following sensors, calculators, and visual aids must be integrated to generate a solution:
-
 Gyrocompass: This device provides an accurate true north own ship course.
@@ -117,3 +137,4 @@
 Plotting board: A map of the gunnery platform and target that allowed predictions to be made as to the future position of a target.
-(The compartment ("room") where the Mk.1 and Mk.1A computers was located was called "Plot" for historical reasons.) Various slide rules: These devices performed the various calculations required to determine the required gun azimuth and elevation.
+(The compartment ("room") where the Mk.1 and Mk.1A computers was located was called "Plot" for historical reasons.)
+Various slide rules: These devices performed the various calculations required to determine the required gun azimuth and elevation.
 Meteorological sensors: Temperature, wind speed, and humidity all have an effect on the ballistics of a projectile.
@@ -121,6 +142,4 @@
 Navy rangekeepers and analog computers did not consider different wind speeds at differing altitudes.
-
 To increase speed and reduce errors, the military felt a dire need to automate these calculations.
 To illustrate the complexity, Table 1 lists the types of input for the Ford Mk 1 Rangekeeper (ca 1931).
-
 However, even with all this data, the rangekeeper's position predictions were not infallible.
@@ -160,3 +179,2 @@
 Some examples include:
-
 Addition and subtraction Differential gears, usually referred to by technicians simply as "differentials", were often used to perform addition and subtraction operations.
@@ -168,3 +186,4 @@
 1 and Mk.1A computer multipliers were based on the geometry of similar triangles.
-Sine and cosine generation (polar-to-rectangular coordinate conversion) These mechanisms would be called resolvers, today; they were called "component solvers" in the mechanical era.
+Sine and cosine generation (polar-to-rectangular coordinate conversion)
+These mechanisms would be called resolvers, today; they were called "component solvers" in the mechanical era.
 In most instances, they resolved an angle and magnitude (radius) into sine and cosine components, with a mechanism consisting of two perpendicular Scotch yokes.
@@ -175,3 +194,2 @@
 1A computers scaled rate-control corrections according to angles.
-
 The integrators had rotating discs and a full-width roller mounted in a hinged casting, pulled down toward the disc by two strong springs.
@@ -199,2 +217,16 @@
 (Superelevation is essentially the amount the gun barrel needs to be raised to compensate for gravity drop.)
+Many eccentrics were used to create variable functions.
+These eccentrics were used in both LVPs.
+The Mk.
+8 Low Velocity Predictor (LVP) used a single eccentric.
+One input is the rotation of an eccentric.
+The other input is the linear position of a repeater ball.
+The radial displacement of the repeater produced an output.
+The Mk.
+1/1A LVP contained four eccentrics.
+The four eccentrics in the Mk.
+1/1A LVP output the time of the mechanical detonator timer.
+The four eccentrics in the Mk.
+1/1A LVP output the elevation correction combined with vertical parallax correction.
+Two strain gauge rollers were located on the sides.
 
@@ -203,2 +235,3 @@
 These were stabilized primarily by rotary magnetic drag (eddy-current) slip clutches, similar to classical rotating-magnet speedometers, but with a much higher torque.
+These couplings are known as eddy current couplings.
 One part of the drag was geared to the motor, and the other was constrained by a fairly stiff spring.
@@ -208,7 +241,9 @@
 A more elaborate scheme, which placed a rather large flywheel and differential between the motor and the magnetic drag, eliminated velocity error for critical data, such as gun orders.
-
-The Mk.
-1 and Mk.
-1A computer integrator discs required a particularly elaborate system to provide constant and precise drive speeds.
+The Mk.
+1/1A included a speed corrector that followed the target.
+The Mk.
+1 and Mk.1A computer integrator discs required a particularly elaborate system to provide constant and precise drive speeds.
 They used a motor with its speed regulated by a clock escapement, cam-operated contacts, and a jeweled-bearing spur-gear differential.
+The motor used a synchronization ramp scheme.
+The motor used a differential with a cylindrical spur gear.
 Although the speed oscillated slightly, the total inertia made it effectively a constant-speed motor.
@@ -224,5 +259,7 @@
 Rangekeepers were only one member of a class of electromechanical computers used for fire control during World War II.
+The most sophisticated of these computers were installed on battleships.
 Related analog computing hardware used by the United States included: Norden bombsight US bombers used the Norden bombsight, which used similar technology to the rangekeeper for predicting bomb impact points.
 Torpedo Data Computer (TDC) US submarines used the TDC to compute torpedo launch angles.
-This device also had a rangekeeping function that was referred to as "position keeping." This was the only submarine-based fire control computer during World War II that performed target tracking.
+This device also had a rangekeeping function that was referred to as "position keeping."
+This was the only submarine-based fire control computer during World War II that performed target tracking.
 Because space within a submarine hull is limited, the TDC designers overcame significant packaging challenges in order to mount the TDC within the allocated volume.
@@ -230,2 +267,25 @@
 It made a particularly good account of itself against the V-1 flying bombs.
+The Computing-Decision Instrument (CDI) or computing-decision device is a historical term.
+These devices were primarily of military purpose.
+They were used for high-altitude bomb dropping.
+They were used for other military tasks requiring complex calculations.
+The S-25 Berkut air defense system was adopted by the Soviet Union in 1955.
+The S-25 Berkut system processed data from radar systems.
+The S-25 Berkut system controlled rockets using a computing device.
+S.
+L.
+Beria was the chief designer.
+P.
+N.
+Kuksenko was the chief designer.
+A.
+A.
+Raspletin was the deputy chief designer.
+The LVP were used to destroy targets on land.
+The LVP were used to destroy targets at sea.
+The most complex computing and firing control devices (LVP) were installed on battleships.
+They were used to control fire from main caliber guns.
+The LVP was partially used in the navy.
+PUAZO systems were used in Soviet anti-aircraft artillery.
+PUAZO-6 is an example of a PUAZO system.
 
@@ -235,2 +295,3 @@
 British fire control British fire control expert Ford Instrument Company museum site.
+There is a museum site dedicated to British fire control.
 Ford built rangekeepers for the US Navy during World Wars I and II OP1140, a superb Navy manual.
```