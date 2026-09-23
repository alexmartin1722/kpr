# Document diff — Mathematical descriptions of the electromagnetic field
*Sentence-level diff, original English → after the KPR merge. 164 lines added/changed.*

```diff
--- Mathematical_descriptions_of_the_electromagnetic_field (original English)
+++ Mathematical_descriptions_of_the_electromagnetic_field (after KPR merge)
@@ -2,2 +2,7 @@
 In this article, several approaches are discussed, although the equations are in terms of electric and magnetic fields, potentials, and charges with currents, generally speaking.
+
+== History ==
+
+James Clerk Maxwell published the complete form of Maxwell's equations in 1865 in a work titled 'A Dynamical Theory of the Electromagnetic Field'.
+Albert Einstein published a paper on special relativity in 1905 titled 'On the Electrodynamics of Moving Bodies'.
 
@@ -11,9 +16,21 @@
 
+== Lorentz force ==
+
+The force vector F is equal to the sum of the electric field vector E and the magnetic force term IcB.
+
 The behaviour of electric and magnetic fields, whether in cases of electrostatics, magnetostatics, or electrodynamics (electromagnetic fields), is governed by Maxwell-Heaviside's equations:
-
 where ρ is the charge density, which can (and often does) depend on time and position, ε₀ is the electric constant, μ₀ is the magnetic constant, and J is the current per unit area, also a function of time and position.
 The equations take this form with the International System of Quantities.
-
+The electromagnetic wave equation involves the speed of light, the permittivity of free space, and the permeability of free space.
+The time derivative term is -1/c^2 times the partial derivative of E_y with respect to t.
+The spatial derivative terms are - the partial derivative of B_z with respect to x plus the partial derivative of B_x with respect to z.
+The source term equals mu_0 times J^2, where J^2 is equivalent to J_y.
+The equation represents the third component of the Maxwell-Ampère law.
 When dealing with only nondispersive isotropic linear materials, Maxwell's equations are often modified to ignore bound charges by replacing the permeability and permittivity of free space with the permeability and permittivity of the linear material in question.
 For some materials that have more complex responses to electromagnetic fields, these properties can be represented by tensors, with time-dependence related to the material's ability to respond to rapid field changes (dispersion (optics), Green–Kubo relations), and possibly also field dependencies representing nonlinear and/or nonlocal material responses to large amplitude fields (nonlinear optics).
+
+== Solutions ==
+
+The first solution has no physical meaning.
+Physicists prefer the second solution.
 
@@ -22,3 +39,4 @@
 This is why sometimes the electric potential is called the scalar potential and the magnetic potential is called the vector potential.
-These potentials can be used to find their associated fields as follows:
+These potentials can be used to find their associated fields as follows: the electric field E is equal to the negative gradient of the scalar potential phi minus the partial derivative of the vector potential A with respect to time, and the magnetic field B is equal to the curl of the vector potential A.
+The electric field E is equal to the negative gradient of V minus the partial derivative of A with respect to time, and the magnetic field B is equal to the curl of A.
 
@@ -29,2 +47,6 @@
 The other two of Maxwell's equations (the inhomogeneous equations) are the ones that describe the dynamics in the potential formulation.
+Two of Maxwell's equations become more complex.
+The equation for the scalar potential V is given by \nabla^2 V + \frac{\partial}{\partial t} (\nabla \cdot \mathbf A) = - \frac{\rho}{\varepsilon_0}.
+The equation represents one of Maxwell's equations.
+The potential field formulation involves second-order derivatives.
 
@@ -38,3 +60,10 @@
 Specifically for these equations, for any choice of a twice-differentiable scalar function of position and time λ, if is a solution for a given system, then so is another potential given by:
-
+The scalar potential can be changed to V', where V' is equal to V minus the partial derivative of lambda with respect to time.
+The vector potential can be changed to A prime, where A prime is equal to A plus the gradient of lambda.
+The transformed magnetic field B' is equal to the curl of the transformed vector potential A'.
+The curl of the transformed vector potential A' equals the curl of the original vector potential A plus the curl of the gradient of lambda.
+The curl of the gradient of lambda is zero.
+Therefore, the transformed magnetic field B' equals the original magnetic field B.
+The transformed electric field E' is defined as the negative gradient of the transformed scalar potential V' minus the partial time derivative of the transformed vector potential A'.
+The term involving the partial time derivative of the gradient of lambda cancels out in the expression for E'.
 This freedom can be used to simplify the potential formulation.
@@ -44,5 +73,5 @@
 In terms of λ, this means that it must satisfy the equation
-
 This choice of function results in the following formulation of Maxwell's equations:
-
+This choice leads to two potential field equations.
+The first equation is the Poisson equation for electric potential: ∇²V = -ρ/ε₀.
 Several features about Maxwell's equations in the Coulomb gauge are as follows.
@@ -50,7 +79,12 @@
 Secondly, solving for the magnetic vector potential is particularly difficult.
+The magnetic vector potential equation is time-dependent.
 This is the big disadvantage of this gauge.
 The third thing to note, and something which is not immediately obvious, is that the electric potential changes instantly everywhere in response to a change in conditions in one locality.
-
+A change in a local source charge occurs.
+This phenomenon is known as action at a distance.
 For instance, if a charge is moved in New York at 1 pm local time, then a hypothetical observer in Australia who could measure the electric potential directly would measure a change in the potential at 1 pm New York time.
 This seemingly violates causality in special relativity, i.e. the impossibility of information, signals, or anything travelling faster than the speed of light.
+The Coulomb gauge is not fully compatible with special relativity.
+When changing reference frames, a Lorentz transformation removes the Coulomb gauge of the original reference frame.
+The Coulomb gauge must then be re-imposed.
 The resolution to this apparent problem lies in the fact that, as previously stated, no observers can measure the potentials; they measure the electric and magnetic fields.
@@ -59,12 +93,11 @@
 A gauge that is often used is the Lorenz gauge condition.
+This gauge freedom is called the Lorenz gauge.
 In this, the scalar function λ is chosen such that
-
 meaning that λ must satisfy the equation
-
+This choice satisfies the condition that the divergence of A equals negative mu-naught epsilon-naught times the partial derivative of V with respect to time.
 The Lorenz gauge results in the following form of Maxwell's equations:
-
 The operator \Box^2 is called the d'Alembertian (some authors denote this by only the square \Box).
+The d'Alembertian operator applied to V is denoted as Box squared V.
 These equations are inhomogeneous versions of the wave equation, with the terms on the right side of the equation serving as the source functions for the wave.
 As with any wave equation, these equations lead to two types of solution: advanced potentials (which are related to the configuration of the sources at future points in time), and retarded potentials (which are related to the past configurations of the sources); the former are usually disregarded where the field is to analyzed from a causality perspective.
-
 As pointed out above, the Lorenz gauge is no more valid than any other gauge since the potentials cannot be directly measured, however the Lorenz gauge has the advantage of the equations being Lorentz invariant.
@@ -84,2 +117,6 @@
 In geometric algebra (GA) these are multivectors which sometimes follow Ricci calculus.
+The symbol boldsymbol{\nabla} is equal to sigma^k partial_k.
+The gradient of a vector field F is equal to the sum of its divergence and its curl.
+The wedge product of the del operator and F (∇ ∧ F) represents the curl component.
+The curl of F is represented by the symbol I ∇ × F.
 
@@ -234,2 +271,12 @@
 Following are the reasons for using each of such formulations.
+Einstein discussed the problem of a moving magnet and conductor in his 1905 paper.
+The scenario assumes a fixed circular wire loop and that the magnet moves at a constant speed.
+The magnetic flux passing through the wire loop changes over time.
+Faraday's law of electromagnetic induction applies, generating an induced electromotive force and producing a corresponding electric field.
+Electric current flows through the ring-shaped wire.
+In a second case, the circular wire moves at a constant speed while the magnet is stationary.
+Charges inside the circular wire experience the Lorentz force, generating a motional electromotive force in the circular wire.
+Current flows through the circular wire.
+The rate of movement is equal in both cases, while the direction of movement is opposite in both cases.
+The induced current is the same in both cases.
 
@@ -268,4 +315,107 @@
 
-For this reason and others, it is often useful to rewrite Maxwell's equations in a way that is "manifestly covariant"—i.e. obviously consistent with special relativity, even with just a glance at the equations—using covariant and contravariant four-vectors and tensors.
+For this reason and others, it is often useful to rewrite Maxwell's equations in a way that is "manifestly covariant"—i.e.
+obviously consistent with special relativity, even with just a glance at the equations—using covariant and contravariant four-vectors and tensors.
 This can be done using the EM tensor F, or the 4-potential A, with the 4-current J.
+
+== Historical context and relativistic consistency ==
+
+The compatibility between the equations and special relativity was surprising.
+According to special relativity, the coincidence is not actually a coincidence.
+Most of Einstein's 1905 paper explained how to transform Maxwell's equations.
+The problem of a moving magnet and conductor is a classic example.
+The electromagnetic tensor aggregates electric and magnetic fields into a single equation.
+The electromagnetic tensor aggregates the electric field and the magnetic field.
+
+== Lorentz transformation of electric and magnetic fields ==
+
+The Lorentz transformation can be used to transform electric and magnetic fields when changing from a reference frame S1 to another reference frame S2 moving at a relative velocity v.
+This transformation involves the Lorentz factor gamma, which is defined as 1 divided by the square root of (1 minus v squared divided by c squared).
+The transformation includes a term involving the cross product of velocity and electric field divided by c squared and a term dependent on the dot product of B and v scaled by (gamma minus 1) over v squared.
+The relative motion is along the x-axis, where the velocity vector v is equal to v times the unit vector in the x-direction.
+The transformation equation for the x-component of the electric field is E-bar sub x equals E sub x.
+The transformation equation for the y-component of the electric field is E-bar sub y equals gamma times (E sub y minus v times B sub z).
+The transformation equation for the z-component of the electric field is E-bar sub z equals gamma times (E sub z plus v times B sub y).
+The transformation equation for the x-component of the magnetic field is B-bar sub x equals B sub x.
+The transformation equation for the y-component of the magnetic field is B-bar sub y equals gamma times (B sub y plus v over c squared times E sub z).
+The transformation equation for the z-component of the magnetic field is B-bar sub z equals gamma times (B sub z minus v over c squared times E sub y).
+The fact that a field is zero in one reference frame does not imply it is zero in all other reference frames.
+If the electric field E is zero in a given reference frame, specific values for the transformed fields can be calculated.
+If E = 0, then the transformed x-component of the electric field (E_x_bar) is equal to 0.
+If E = 0, then the transformed y-component of the electric field (E_y_bar) is equal to negative gamma times v times B_z.
+If E = 0, then the transformed z-component of the electric field (E_z_bar) is equal to gamma times v times B_y.
+If E = 0, then the transformed x-component of the magnetic field (B_x_bar) is equal to B_x.
+
+If E = 0, then the transformed y-component of the magnetic field (B_y_bar) is equal to gamma times B_y.
+
+== The electromagnetic field tensor ==
+
+The equation defines the electromagnetic tensor as $F_{\alpha \beta}$, which is an n-rank covariant tensor.
+The matrix element at row 1, column 2 is $E_x$ divided by $c$, while the element at row 2, column 1 is negative $E_x$ divided by $c$.
+The matrix element at row 2, column 3 is negative $B_z$, and the element at row 2, column 4 is $B_y$.
+The matrix element at row 3, column 1 is negative $E_y$ divided by $c$, while the element at row 3, column 2 is $B_z$.
+The matrix element at row 4, column 1 is negative $E_z$ divided by $c$, the element at row 4, column 2 is negative $B_y$, and the element at row 4, column 3 is $B_x$.
+
+== The Minkowski metric and index raising ==
+
+The Minkowski metric is denoted by the symbol eta, and its contravariant components are given by eta to the power of alpha beta.
+The matrix representation of the Minkowski metric is diagonal, with the time component being positive one and the spatial components being negative one.
+Raising the indices of F_{\alpha \beta} yields the contravariant tensor F^{\mu \nu}, a procedure expressed as F^{\mu \nu} = \eta^{\alpha\mu} \, \eta^{\beta \nu} \, F_{\alpha \beta}.
+
+== Contravariant electromagnetic tensor components ==
+
+The element at row 1, column 2 of the matrix is -E_x/c, and the element at row 1, column 3 is -E_y/c.
+The element at row 2, column 1 of the matrix is E_x/c, the element at row 2, column 3 is -B_z, and the element at row 2, column 4 is B_y.
+The element at row 3, column 1 of the matrix is E_y/c, the element at row 3, column 2 is B_z, and the element at row 3, column 4 is -B_x.
+The element at row 4, column 1 of the matrix is E_z/c, the element at row 4, column 2 is -B_y, and the element at row 4, column 3 is B_x.
+
+== The dual electromagnetic tensor ==
+
+G is a contravariant tensor and is antisymmetric.
+The components of G are defined by a formula involving the Levi-Civita symbol and F.
+The symbol epsilon with superscript indices j1, j2, ..., jm, i1, i2, ..., in is the Levi-Civita symbol, which has m + n dimensions.
+The second-rank dual tensor G^{\mu \nu} of F_{\alpha \beta} is defined as shown.
+The component G^{01} equals -B_x, the component G^{02} equals -B_y, the component G^{10} equals B_x, and the component G^{20} equals B_y.
+
+== Lorentz transformation matrix and four-vectors ==
+
+Two inertial reference frames, S and S-bar, are given, where reference frame S-bar moves relative to reference frame S with velocity v in the x-direction.
+The Lorentz transformation matrix Lambda connecting these two reference frames is defined as a 4x4 matrix with the element at row 1, column 1 being gamma, the element at row 1, column 2 being negative gamma beta, the element at row 2, column 1 being negative gamma beta, and the element at row 2, column 2 being gamma.
+The elements at row 3, columns 1 through 4 are 0, 0, 1, and 0 respectively, while the elements at row 4, columns 1 through 4 are 0, 0, 0, and 1 respectively.
+The symbol gamma represents the Lorentz factor, and the symbol beta represents the beta factor, which is defined by the formula v divided by c.
+The four-dimensional position of an event in the first frame is denoted as x^\mu, and the four-dimensional position of the same event in the second frame is denoted as \bar{x}^\mu.
+The relationship between these two four-dimensional positions is given by the equation \bar{x}^\mu = \Lambda^\mu_{\nu}x^\nu.
+
+== Tensor transformation laws ==
+
+In relativity, the electromagnetic tensor and its dual tensor can be transformed from one reference frame to another using Lorentz transformations.
+The transformation of the electromagnetic tensor is expressed by the equation $\bar{F}^{\alpha \beta} = \Lambda^\alpha_\mu \Lambda^\beta_\nu F^{\mu \nu}$.
+The transformation of the dual electromagnetic tensor is expressed by the equation $\bar{G}^{\alpha \beta} = \Lambda^\alpha_\mu \Lambda^\beta_\nu G^{\mu \nu}$.
+
+== Maxwell's equations in tensor form ==
+
+One form of the Maxwell equations is given by the equation {F^{\alpha \beta}}_{,\alpha} = \mu_0 J^\beta.
+Another form of the Maxwell equations is given by the equation {G^{\alpha \beta}}_{,\alpha} = 0.
+
+== Derivation of Gauss's laws ==
+
+Setting beta equal to zero allows deriving Gauss's law from Maxwell's equations involving the tensor F^alpha beta.
+The derived equation is {F^{alpha 0}}_{,alpha} = (1/c)(dEx/dx + dEy/dy + dEz/dz) = mu_0 J^0 = mu_0 c rho.
+The Maxwell equations derived from the tensor G^{\alpha \beta} yield Gauss's law for magnetism.
+Gauss's law for magnetism is expressed as {G^{\alpha 0}}_{,\alpha} = 0.
+The term {G^{\alpha 0}}_{,\alpha} equals (1/c) times the sum of the partial derivatives of the magnetic field components with respect to their spatial coordinates.
+The equation states that the divergence of the magnetic field vector (B_x, B_y, B_z) is zero.
+
+== Derivation of the Maxwell-Ampère law ==
+
+There are three Maxwell equations corresponding to the Maxwell-Ampère law.
+These equations involve indices where beta equals 1, 2, or 3.
+The partial derivative of F with respect to alpha equals negative one over c squared times the partial derivative of Ex with respect to t plus the partial derivative of Bz with respect to y minus the partial derivative of By with respect to z, and this expression equals mu naught times J superscript 1, where J superscript 1 is equivalent to J subscript x.
+The divergence of the electromagnetic field tensor component F^{alpha 3} with respect to alpha equals negative one over c squared times the partial derivative of E_z with respect to t plus the partial derivative of B_y with respect to x minus the partial derivative of B_x with respect to y, and this expression is equal to mu_0 times J^3, where J^3 is equivalent to J_z.
+
+== Derivation of Faraday's law ==
+
+The three Maxwell equations for $G^{\alpha \beta}$ correspond to Faraday's law of electromagnetic induction.
+The first equation includes the term $-\partial B_x / \partial t$, the term $-\partial E_z / (c \partial y)$, and the term $+\partial E_y / (c \partial z)$.
+The equation for $G^{\alpha 2}_{,\alpha}$ equals the negative partial derivative of $B_y$ with respect to $t$ plus the partial derivative of $E_z$ divided by $c$ with respect to $x$ minus the partial derivative of $E_x$ divided by $c$ with respect to $z$ equals zero.
+This equation includes the term negative partial $B_z$ with respect to $t$, the term negative partial $E_y$ with respect to $c$ times $x$, and the term positive partial $E_x$ with respect to $c$ times $y$.
 
@@ -292 +442,3 @@
 Ricci calculus Electromagnetic wave equation Speed of light Electric constant Magnetic constant Free space Near and far field Electromagnetic field Electromagnetic radiation Quantum electrodynamics List of electromagnetism equations
+
+The source of the worked problems is Warnick and Russer, 2006.
```