# Mathematical descriptions of the electromagnetic field

There are various mathematical descriptions of the electromagnetic field that are used in the study of electromagnetism, one of the four fundamental interactions of nature. In this article, several approaches are discussed, although the equations are in terms of electric and magnetic fields, potentials, and charges with currents, generally speaking.

== History ==

James Clerk Maxwell published the complete form of Maxwell's equations in 1865 in a work titled 'A Dynamical Theory of the Electromagnetic Field'.
Albert Einstein published a paper on special relativity in 1905 titled 'On the Electrodynamics of Moving Bodies'.

The most common description of the electromagnetic field uses two three-dimensional vector fields called the electric field and the magnetic field. These vector fields each have a value defined at every point of space and time and are thus often regarded as functions of the space and time coordinates. As such, they are often written as (electric field) and (magnetic field).

If only the electric field (E) is non-zero, and is constant in time, the field is said to be an electrostatic field. Similarly, if only the magnetic field (B) is non-zero and is constant in time, the field is said to be a magnetostatic field. However, if either the electric or magnetic field has a time-dependence, then both fields must be considered together as a coupled electromagnetic field using Maxwell's equations.

== Lorentz force ==

The force vector F is equal to the sum of the electric field vector E and the magnetic force term IcB.

The behaviour of electric and magnetic fields, whether in cases of electrostatics, magnetostatics, or electrodynamics (electromagnetic fields), is governed by Maxwell-Heaviside's equations:
where ρ is the charge density, which can (and often does) depend on time and position, ε₀ is the electric constant, μ₀ is the magnetic constant, and J is the current per unit area, also a function of time and position.
The equations take this form with the International System of Quantities.
The electromagnetic wave equation involves the speed of light, the permittivity of free space, and the permeability of free space.
The time derivative term is -1/c^2 times the partial derivative of E_y with respect to t.
The spatial derivative terms are - the partial derivative of B_z with respect to x plus the partial derivative of B_x with respect to z.
The source term equals mu_0 times J^2, where J^2 is equivalent to J_y.
The equation represents the third component of the Maxwell-Ampère law.
When dealing with only nondispersive isotropic linear materials, Maxwell's equations are often modified to ignore bound charges by replacing the permeability and permittivity of free space with the permeability and permittivity of the linear material in question.
For some materials that have more complex responses to electromagnetic fields, these properties can be represented by tensors, with time-dependence related to the material's ability to respond to rapid field changes (dispersion (optics), Green–Kubo relations), and possibly also field dependencies representing nonlinear and/or nonlocal material responses to large amplitude fields (nonlinear optics).

== Solutions ==

The first solution has no physical meaning.
Physicists prefer the second solution.

Many times in the use and calculation of electric and magnetic fields, the approach used first computes an associated potential: the electric potential, \varphi, for the electric field, and the magnetic vector potential, A, for the magnetic field.
The electric potential is a scalar field, while the magnetic potential is a vector field.
This is why sometimes the electric potential is called the scalar potential and the magnetic potential is called the vector potential.
These potentials can be used to find their associated fields as follows: the electric field E is equal to the negative gradient of the scalar potential phi minus the partial derivative of the vector potential A with respect to time, and the magnetic field B is equal to the curl of the vector potential A.
The electric field E is equal to the negative gradient of V minus the partial derivative of A with respect to time, and the magnetic field B is equal to the curl of A.

These relations can be substituted into Maxwell's equations to express the latter in terms of the potentials.
Faraday's law and Gauss's law for magnetism (the homogeneous equations) turn out to be identically true for any potentials.
This is because of the way the fields are expressed as gradients and curls of the scalar and vector potentials.
The homogeneous equations in terms of these potentials involve the divergence of the curl \nabla \cdot \nabla \times \mathbf A and the curl of the gradient \nabla \times \nabla \varphi, which are always zero.
The other two of Maxwell's equations (the inhomogeneous equations) are the ones that describe the dynamics in the potential formulation.
Two of Maxwell's equations become more complex.
The equation for the scalar potential V is given by \nabla^2 V + \frac{\partial}{\partial t} (\nabla \cdot \mathbf A) = - \frac{\rho}{\varepsilon_0}.
The equation represents one of Maxwell's equations.
The potential field formulation involves second-order derivatives.

These equations taken together are as powerful and complete as Maxwell's equations.
Moreover, the problem has been reduced somewhat, as the electric and magnetic fields together had six components to solve for.
In the potential formulation, there are only four components: the electric potential and the three components of the vector potential.
However, the equations are messier than Maxwell's equations using the electric and magnetic fields.

These equations can be simplified by taking advantage of the fact that the electric and magnetic fields are physically meaningful quantities that can be measured; the potentials are not.
There is a freedom to constrain the form of the potentials provided that this does not affect the resultant electric and magnetic fields, called gauge freedom.
Specifically for these equations, for any choice of a twice-differentiable scalar function of position and time λ, if is a solution for a given system, then so is another potential given by:
The scalar potential can be changed to V', where V' is equal to V minus the partial derivative of lambda with respect to time.
The vector potential can be changed to A prime, where A prime is equal to A plus the gradient of lambda.
The transformed magnetic field B' is equal to the curl of the transformed vector potential A'.
The curl of the transformed vector potential A' equals the curl of the original vector potential A plus the curl of the gradient of lambda.
The curl of the gradient of lambda is zero.
Therefore, the transformed magnetic field B' equals the original magnetic field B.
The transformed electric field E' is defined as the negative gradient of the transformed scalar potential V' minus the partial time derivative of the transformed vector potential A'.
The term involving the partial time derivative of the gradient of lambda cancels out in the expression for E'.
This freedom can be used to simplify the potential formulation.
Either of two such scalar functions is typically chosen: the Coulomb gauge and the Lorenz gauge.

The Coulomb gauge is chosen in such a way that \mathbf \nabla \cdot \mathbf A' = 0, which corresponds to the case of magnetostatics.
In terms of λ, this means that it must satisfy the equation
This choice of function results in the following formulation of Maxwell's equations:
This choice leads to two potential field equations.
The first equation is the Poisson equation for electric potential: ∇²V = -ρ/ε₀.
Several features about Maxwell's equations in the Coulomb gauge are as follows.
Firstly, solving for the electric potential is very easy, as the equation is a version of Poisson's equation.
Secondly, solving for the magnetic vector potential is particularly difficult.
The magnetic vector potential equation is time-dependent.
This is the big disadvantage of this gauge.
The third thing to note, and something which is not immediately obvious, is that the electric potential changes instantly everywhere in response to a change in conditions in one locality.
A change in a local source charge occurs.
This phenomenon is known as action at a distance.
For instance, if a charge is moved in New York at 1 pm local time, then a hypothetical observer in Australia who could measure the electric potential directly would measure a change in the potential at 1 pm New York time.
This seemingly violates causality in special relativity, i.e. the impossibility of information, signals, or anything travelling faster than the speed of light.
The Coulomb gauge is not fully compatible with special relativity.
When changing reference frames, a Lorentz transformation removes the Coulomb gauge of the original reference frame.
The Coulomb gauge must then be re-imposed.
The resolution to this apparent problem lies in the fact that, as previously stated, no observers can measure the potentials; they measure the electric and magnetic fields.
So, the combination of ∇φ and ∂A/∂t used in determining the electric field restores the speed limit imposed by special relativity for the electric field, making all observable quantities consistent with relativity.

A gauge that is often used is the Lorenz gauge condition.
This gauge freedom is called the Lorenz gauge.
In this, the scalar function λ is chosen such that
meaning that λ must satisfy the equation
This choice satisfies the condition that the divergence of A equals negative mu-naught epsilon-naught times the partial derivative of V with respect to time.
The Lorenz gauge results in the following form of Maxwell's equations:
The operator \Box^2 is called the d'Alembertian (some authors denote this by only the square \Box).
The d'Alembertian operator applied to V is denoted as Box squared V.
These equations are inhomogeneous versions of the wave equation, with the terms on the right side of the equation serving as the source functions for the wave.
As with any wave equation, these equations lead to two types of solution: advanced potentials (which are related to the configuration of the sources at future points in time), and retarded potentials (which are related to the past configurations of the sources); the former are usually disregarded where the field is to analyzed from a causality perspective.
As pointed out above, the Lorenz gauge is no more valid than any other gauge since the potentials cannot be directly measured, however the Lorenz gauge has the advantage of the equations being Lorentz invariant.

Canonical quantization of the electromagnetic fields proceeds by elevating the scalar and vector potentials; φ(x), A(x), from fields to field operators. Substituting into the previous Lorenz gauge equations gives:

Here, J and ρ are the current and charge density of the matter field. If the matter field is taken so as to describe the interaction of electromagnetic fields with the Dirac electron given by the four-component Dirac spinor field ψ, the current and charge densities have form:

where α are the first three Dirac matrices. Using this, we can re-write Maxwell's equations as:

which is the form used in quantum electrodynamics.

Analogous to the tensor formulation, two objects, one for the electromagnetic field and one for the current density, are introduced.
In geometric algebra (GA) these are multivectors which sometimes follow Ricci calculus.
The symbol boldsymbol{\nabla} is equal to sigma^k partial_k.
The gradient of a vector field F is equal to the sum of its divergence and its curl.
The wedge product of the del operator and F (∇ ∧ F) represents the curl component.
The curl of F is represented by the symbol I ∇ × F.

In the Algebra of physical space (APS), also known as the Clifford algebra C\ell_{3,0}(\R), the field and current are represented by multivectors.

The field multivector, known as the Riemann–Silberstein vector, is

and the four-current multivector is

using an orthonormal basis \{\sigma_k\}. Similarly, the unit pseudoscalar is I=\sigma_1\sigma_2\sigma_3, due to the fact that the basis used is orthonormal. These basis vectors share the algebra of the Pauli matrices, but are usually not equated with them, as they are different objects with different interpretations.

After defining the derivative

Maxwell's equations are reduced to the single equation

In three dimensions, the derivative has a special structure allowing the introduction of a cross product:

from which it is easily seen that Gauss's law is the scalar part, the Ampère–Maxwell law is the vector part, Faraday's law is the pseudovector part, and Gauss's law for magnetism is the pseudoscalar part of the equation. After expanding and rearranging, this can be written as

We can identify APS as a subalgebra of the spacetime algebra (STA) C\ell_{1,3}(\mathbb{R}), defining \sigma_k=\gamma_k\gamma_0 and I=\gamma_0\gamma_1\gamma_2\gamma_3. The \gamma_\mus have the same algebraic properties of the gamma matrices but their matrix representation is not needed. The derivative is now

The Riemann–Silberstein becomes a bivector

and the charge and current density become a vector

Owing to the identity

Maxwell's equations reduce to the single equation

In what follows, cgs-Gaussian units, not SI units are used. (To convert to SI, see here.) By Einstein notation, we implicitly take the sum over all values of the indices that can vary within the dimension.

In free space, where and are constant everywhere, Maxwell's equations simplify considerably once the language of differential geometry and differential forms is used. The electric and magnetic fields are now jointly described by a 2-form F in a 4-dimensional spacetime manifold. The Faraday tensor F_{\mu\nu} (electromagnetic tensor) can be written as a 2-form in Minkowski space with metric signature as

which is the exterior derivative of the electromagnetic four-potential \mathbf{A} :

The source free equations can be written by the action of the exterior derivative on this 2-form. But for the equations with source terms (Gauss's law and the Ampère-Maxwell equation), the Hodge dual of this 2-form is needed. The Hodge star operator takes a p-form to a ()-form, where n is the number of dimensions. Here, it takes the 2-form (F) and gives another 2-form (in four dimensions, ). For the basis cotangent vectors, the Hodge dual is given as (see )

and so on. Using these relations, the dual of the Faraday 2-form is the Maxwell tensor,

Here, the 3-form J is called the electric current form or current 3-form:

That F is a closed form, and the exterior derivative of its Hodge dual is the current 3-form, express Maxwell's equations:

Here d denotes the exterior derivative – a natural coordinate- and metric-independent differential operator acting on forms, and the (dual) Hodge star operator {\star} is a linear transformation from the space of 2-forms to the space of (4 − 2)-forms defined by the metric in Minkowski space (in four dimensions even by any metric conformal to this metric). The fields are in natural units where .

Since d² = 0, the 3-form J satisfies the conservation of current (continuity equation):

The current 3-form can be integrated over a 3-dimensional space-time region. The physical interpretation of this integral is the charge in that region if it is spacelike, or the amount of charge that flows through a surface in a certain amount of time if that region is a spacelike surface cross a timelike interval. As the exterior derivative is defined on any manifold, the differential form version of the Bianchi identity makes sense for any 4-dimensional manifold, whereas the source equation is defined if the manifold is oriented and has a Lorentz metric. In particular the differential form version of the Maxwell equations are a convenient and intuitive formulation of the Maxwell equations in general relativity.

Note: In much of the literature, the notations \mathbf{J} and {\star}\mathbf{J} are switched, so that \mathbf{J} is a 1-form called the current and {\star}\mathbf{J} is a 3-form called the dual current.

In a linear, macroscopic theory, the influence of matter on the electromagnetic field is described through more general linear transformation in the space of 2-forms. We call

the constitutive transformation. The role of this transformation is comparable to the Hodge duality transformation. The Maxwell equations in the presence of matter then become:

where the current 3-form J still satisfies the continuity equation .

When the fields are expressed as linear combinations (of exterior products) of basis forms θⁱ,

the constitutive relation takes the form

where the field coefficient functions and the constitutive coefficients are anticommutative for swapping of each one's indices. In particular, the Hodge star operator which was used in the above case is obtained by taking

in terms of tensor index notation with respect to a (not necessarily orthonormal) basis \left\{\frac{\partial}{\partial x_1}, \ldots, \frac{\partial}{\partial x_n}\right\} in a tangent space V = T_p M and its dual basis \{dx_1,\ldots,dx_n\} in V^* = T^*_p M, having the gram metric matrix (g_{ij}) = \left(\left\langle \frac{\partial}{\partial x_i}, \frac{\partial}{\partial x_j}\right\rangle\right) and its inverse matrix (g^{ij}) = (\langle dx^i, dx^j\rangle), and \varepsilon_{abpq} is the Levi-Civita symbol with \varepsilon_{1234} = 1. Up to scaling, this is the only invariant tensor of this type that can be defined with the metric.

In this formulation, electromagnetism generalises immediately to any 4-dimensional oriented manifold or with small adaptations any manifold.

In the particle physicist's sign convention for the metric signature , the potential 1-form is

The Faraday curvature 2-form becomes

and the Maxwell tensor becomes

The current 3-form J is

and the corresponding dual 1-form is

The current norm is now positive and equals

with the canonical volume form {\star}(1) = \mathrm{d}t \wedge \mathrm{d}x \wedge \mathrm{d}y \wedge \mathrm{d}z.

Matter and energy generate curvature of spacetime. This is the subject of general relativity. Curvature of spacetime affects electrodynamics. An electromagnetic field having energy and momentum also generates curvature in spacetime. Maxwell's equations in curved spacetime can be obtained by replacing the derivatives in the equations in flat spacetime with covariant derivatives. (Whether this is the appropriate generalization requires separate investigation.) The sourced and source-free equations become (cgs-Gaussian units):

and

Here,

is a Christoffel symbol that characterizes the curvature of spacetime and ∇α is the covariant derivative.

The formulation of the Maxwell equations in terms of differential forms can be used without change in general relativity. The equivalence of the more traditional general relativistic formulation using the covariant derivative with the differential form formulation can be seen as follows. Choose local coordinates xα which gives a basis of 1-forms dxα in every point of the open set where the coordinates are defined. Using this basis and cgs-Gaussian units we define

The antisymmetric field tensor Fαβ, corresponding to the field 2-form F

The current-vector infinitesimal 3-form J

The epsilon tensor contracted with the differential 3-form produces 6 times the number of terms required.

Here g is as usual the determinant of the matrix representing the metric tensor, gαβ. A small computation that uses the symmetry of the Christoffel symbols (i.e., the torsion-freeness of the Levi-Civita connection) and the covariant constantness of the Hodge star operator then shows that in this coordinate neighborhood we have:

the Bianchi identity

the source equation

the continuity equation

An elegant and intuitive way to formulate Maxwell's equations is to use complex line bundles or a principal U(1)-bundle, on the fibers of which U(1) acts regularly. The principal U(1)-connection ∇ on the line bundle has a curvature F = ∇² which is a two-form that automatically satisfies and can be interpreted as a field-strength. If the line bundle is trivial with flat reference connection d we can write and with A the 1-form composed of the electric potential and the magnetic vector potential.

In quantum mechanics, the connection itself is used to define the dynamics of the system. This formulation allows a natural description of the Aharonov–Bohm effect. In this experiment, a static magnetic field runs through a long magnetic wire (e.g., an iron wire magnetized longitudinally). Outside of this wire the magnetic induction is zero, in contrast to the vector potential, which essentially depends on the magnetic flux through the cross-section of the wire and does not vanish outside. Since there is no electric field either, the Maxwell tensor throughout the space-time region outside the tube, during the experiment. This means by definition that the connection ∇ is flat there.

In mentioned Aharonov–Bohm effect, however, the connection depends on the magnetic field through the tube since the holonomy along a non-contractible curve encircling the tube is the magnetic flux through the tube in the proper units. This can be detected quantum-mechanically with a double-slit electron diffraction experiment on an electron wave traveling around the tube. The holonomy corresponds to an extra phase shift, which leads to a shift in the diffraction pattern.

Following are the reasons for using each of such formulations.
Einstein discussed the problem of a moving magnet and conductor in his 1905 paper.
The scenario assumes a fixed circular wire loop and that the magnet moves at a constant speed.
The magnetic flux passing through the wire loop changes over time.
Faraday's law of electromagnetic induction applies, generating an induced electromotive force and producing a corresponding electric field.
Electric current flows through the ring-shaped wire.
In a second case, the circular wire moves at a constant speed while the magnet is stationary.
Charges inside the circular wire experience the Lorentz force, generating a motional electromotive force in the circular wire.
Current flows through the circular wire.
The rate of movement is equal in both cases, while the direction of movement is opposite in both cases.
The induced current is the same in both cases.

In advanced classical mechanics it is often useful, and in quantum mechanics frequently essential, to express Maxwell's equations in a potential formulation involving the electric potential (also called scalar potential) φ, and the magnetic potential (a vector potential) A. For example, the analysis of radio antennas makes full use of Maxwell's vector and scalar potentials to separate the variables, a common technique used in formulating the solutions of differential equations. The potentials can be introduced by using the Poincaré lemma on the homogeneous equations to solve them in a universal way (this assumes that we consider a topologically simple, e.g. contractible space). The potentials are defined as in the table above. Alternatively, these equations define E and B in terms of the electric and magnetic potentials which then satisfy the homogeneous equations for E and B as identities. Substitution gives the non-homogeneous Maxwell equations in potential form.

Many different choices of A and φ are consistent with given observable electric and magnetic fields E and B, so the potentials seem to contain more, (classically) unobservable information. The non uniqueness of the potentials is well understood, however. For every scalar function of position and time , the potentials can be changed by a gauge transformation as

without changing the electric and magnetic field. Two pairs of gauge transformed potentials and are called gauge equivalent, and the freedom to select any pair of potentials in its gauge equivalence class is called gauge freedom. Again by the Poincaré lemma (and under its assumptions), gauge freedom is the only source of indeterminacy, so the field formulation is equivalent to the potential formulation if we consider the potential equations as equations for gauge equivalence classes.

The potential equations can be simplified using a procedure called gauge fixing. Since the potentials are only defined up to gauge equivalence, we are free to impose additional equations on the potentials, as long as for every pair of potentials there is a gauge equivalent pair that satisfies the additional equations (i.e. if the gauge fixing equations define a slice to the gauge action). The gauge-fixed potentials still have a gauge freedom under all gauge transformations that leave the gauge fixing equations invariant. Inspection of the potential equations suggests two natural choices. In the Coulomb gauge, we impose which is mostly used in the case of magneto statics when we can neglect the term. In the Lorenz gauge (named after the Dane Ludvig Lorenz), we impose

The Lorenz gauge condition has the advantage of being Lorentz invariant and leading to Lorentz-invariant equations for the potentials.

Maxwell's equations are exactly consistent with special relativity—i.e., if they are valid in one inertial reference frame, then they are automatically valid in every other inertial reference frame.
In fact, Maxwell's equations were crucial in the historical development of special relativity.
However, in the usual formulation of Maxwell's equations, their consistency with special relativity is not obvious; it can only be proven by a laborious calculation.

For example, consider a conductor moving in the field of a magnet.
In the frame of the magnet, that conductor experiences a magnetic force.
But in the frame of a conductor moving relative to the magnet, the conductor experiences a force due to an electric field.
The motion is exactly consistent in these two different reference frames, but it mathematically arises in quite different ways.

For this reason and others, it is often useful to rewrite Maxwell's equations in a way that is "manifestly covariant"—i.e.
obviously consistent with special relativity, even with just a glance at the equations—using covariant and contravariant four-vectors and tensors.
This can be done using the EM tensor F, or the 4-potential A, with the 4-current J.

== Historical context and relativistic consistency ==

The compatibility between the equations and special relativity was surprising.
According to special relativity, the coincidence is not actually a coincidence.
Most of Einstein's 1905 paper explained how to transform Maxwell's equations.
The problem of a moving magnet and conductor is a classic example.
The electromagnetic tensor aggregates electric and magnetic fields into a single equation.
The electromagnetic tensor aggregates the electric field and the magnetic field.

== Lorentz transformation of electric and magnetic fields ==

The Lorentz transformation can be used to transform electric and magnetic fields when changing from a reference frame S1 to another reference frame S2 moving at a relative velocity v.
This transformation involves the Lorentz factor gamma, which is defined as 1 divided by the square root of (1 minus v squared divided by c squared).
The transformation includes a term involving the cross product of velocity and electric field divided by c squared and a term dependent on the dot product of B and v scaled by (gamma minus 1) over v squared.
The relative motion is along the x-axis, where the velocity vector v is equal to v times the unit vector in the x-direction.
The transformation equation for the x-component of the electric field is E-bar sub x equals E sub x.
The transformation equation for the y-component of the electric field is E-bar sub y equals gamma times (E sub y minus v times B sub z).
The transformation equation for the z-component of the electric field is E-bar sub z equals gamma times (E sub z plus v times B sub y).
The transformation equation for the x-component of the magnetic field is B-bar sub x equals B sub x.
The transformation equation for the y-component of the magnetic field is B-bar sub y equals gamma times (B sub y plus v over c squared times E sub z).
The transformation equation for the z-component of the magnetic field is B-bar sub z equals gamma times (B sub z minus v over c squared times E sub y).
The fact that a field is zero in one reference frame does not imply it is zero in all other reference frames.
If the electric field E is zero in a given reference frame, specific values for the transformed fields can be calculated.
If E = 0, then the transformed x-component of the electric field (E_x_bar) is equal to 0.
If E = 0, then the transformed y-component of the electric field (E_y_bar) is equal to negative gamma times v times B_z.
If E = 0, then the transformed z-component of the electric field (E_z_bar) is equal to gamma times v times B_y.
If E = 0, then the transformed x-component of the magnetic field (B_x_bar) is equal to B_x.

If E = 0, then the transformed y-component of the magnetic field (B_y_bar) is equal to gamma times B_y.

== The electromagnetic field tensor ==

The equation defines the electromagnetic tensor as $F_{\alpha \beta}$, which is an n-rank covariant tensor.
The matrix element at row 1, column 2 is $E_x$ divided by $c$, while the element at row 2, column 1 is negative $E_x$ divided by $c$.
The matrix element at row 2, column 3 is negative $B_z$, and the element at row 2, column 4 is $B_y$.
The matrix element at row 3, column 1 is negative $E_y$ divided by $c$, while the element at row 3, column 2 is $B_z$.
The matrix element at row 4, column 1 is negative $E_z$ divided by $c$, the element at row 4, column 2 is negative $B_y$, and the element at row 4, column 3 is $B_x$.

== The Minkowski metric and index raising ==

The Minkowski metric is denoted by the symbol eta, and its contravariant components are given by eta to the power of alpha beta.
The matrix representation of the Minkowski metric is diagonal, with the time component being positive one and the spatial components being negative one.
Raising the indices of F_{\alpha \beta} yields the contravariant tensor F^{\mu \nu}, a procedure expressed as F^{\mu \nu} = \eta^{\alpha\mu} \, \eta^{\beta \nu} \, F_{\alpha \beta}.

== Contravariant electromagnetic tensor components ==

The element at row 1, column 2 of the matrix is -E_x/c, and the element at row 1, column 3 is -E_y/c.
The element at row 2, column 1 of the matrix is E_x/c, the element at row 2, column 3 is -B_z, and the element at row 2, column 4 is B_y.
The element at row 3, column 1 of the matrix is E_y/c, the element at row 3, column 2 is B_z, and the element at row 3, column 4 is -B_x.
The element at row 4, column 1 of the matrix is E_z/c, the element at row 4, column 2 is -B_y, and the element at row 4, column 3 is B_x.

== The dual electromagnetic tensor ==

G is a contravariant tensor and is antisymmetric.
The components of G are defined by a formula involving the Levi-Civita symbol and F.
The symbol epsilon with superscript indices j1, j2, ..., jm, i1, i2, ..., in is the Levi-Civita symbol, which has m + n dimensions.
The second-rank dual tensor G^{\mu \nu} of F_{\alpha \beta} is defined as shown.
The component G^{01} equals -B_x, the component G^{02} equals -B_y, the component G^{10} equals B_x, and the component G^{20} equals B_y.

== Lorentz transformation matrix and four-vectors ==

Two inertial reference frames, S and S-bar, are given, where reference frame S-bar moves relative to reference frame S with velocity v in the x-direction.
The Lorentz transformation matrix Lambda connecting these two reference frames is defined as a 4x4 matrix with the element at row 1, column 1 being gamma, the element at row 1, column 2 being negative gamma beta, the element at row 2, column 1 being negative gamma beta, and the element at row 2, column 2 being gamma.
The elements at row 3, columns 1 through 4 are 0, 0, 1, and 0 respectively, while the elements at row 4, columns 1 through 4 are 0, 0, 0, and 1 respectively.
The symbol gamma represents the Lorentz factor, and the symbol beta represents the beta factor, which is defined by the formula v divided by c.
The four-dimensional position of an event in the first frame is denoted as x^\mu, and the four-dimensional position of the same event in the second frame is denoted as \bar{x}^\mu.
The relationship between these two four-dimensional positions is given by the equation \bar{x}^\mu = \Lambda^\mu_{\nu}x^\nu.

== Tensor transformation laws ==

In relativity, the electromagnetic tensor and its dual tensor can be transformed from one reference frame to another using Lorentz transformations.
The transformation of the electromagnetic tensor is expressed by the equation $\bar{F}^{\alpha \beta} = \Lambda^\alpha_\mu \Lambda^\beta_\nu F^{\mu \nu}$.
The transformation of the dual electromagnetic tensor is expressed by the equation $\bar{G}^{\alpha \beta} = \Lambda^\alpha_\mu \Lambda^\beta_\nu G^{\mu \nu}$.

== Maxwell's equations in tensor form ==

One form of the Maxwell equations is given by the equation {F^{\alpha \beta}}_{,\alpha} = \mu_0 J^\beta.
Another form of the Maxwell equations is given by the equation {G^{\alpha \beta}}_{,\alpha} = 0.

== Derivation of Gauss's laws ==

Setting beta equal to zero allows deriving Gauss's law from Maxwell's equations involving the tensor F^alpha beta.
The derived equation is {F^{alpha 0}}_{,alpha} = (1/c)(dEx/dx + dEy/dy + dEz/dz) = mu_0 J^0 = mu_0 c rho.
The Maxwell equations derived from the tensor G^{\alpha \beta} yield Gauss's law for magnetism.
Gauss's law for magnetism is expressed as {G^{\alpha 0}}_{,\alpha} = 0.
The term {G^{\alpha 0}}_{,\alpha} equals (1/c) times the sum of the partial derivatives of the magnetic field components with respect to their spatial coordinates.
The equation states that the divergence of the magnetic field vector (B_x, B_y, B_z) is zero.

== Derivation of the Maxwell-Ampère law ==

There are three Maxwell equations corresponding to the Maxwell-Ampère law.
These equations involve indices where beta equals 1, 2, or 3.
The partial derivative of F with respect to alpha equals negative one over c squared times the partial derivative of Ex with respect to t plus the partial derivative of Bz with respect to y minus the partial derivative of By with respect to z, and this expression equals mu naught times J superscript 1, where J superscript 1 is equivalent to J subscript x.
The divergence of the electromagnetic field tensor component F^{alpha 3} with respect to alpha equals negative one over c squared times the partial derivative of E_z with respect to t plus the partial derivative of B_y with respect to x minus the partial derivative of B_x with respect to y, and this expression is equal to mu_0 times J^3, where J^3 is equivalent to J_z.

== Derivation of Faraday's law ==

The three Maxwell equations for $G^{\alpha \beta}$ correspond to Faraday's law of electromagnetic induction.
The first equation includes the term $-\partial B_x / \partial t$, the term $-\partial E_z / (c \partial y)$, and the term $+\partial E_y / (c \partial z)$.
The equation for $G^{\alpha 2}_{,\alpha}$ equals the negative partial derivative of $B_y$ with respect to $t$ plus the partial derivative of $E_z$ divided by $c$ with respect to $x$ minus the partial derivative of $E_x$ divided by $c$ with respect to $z$ equals zero.
This equation includes the term negative partial $B_z$ with respect to $t$, the term negative partial $E_y$ with respect to $c$ times $x$, and the term positive partial $E_x$ with respect to $c$ times $y$.

Gauss's law for magnetism and the Faraday–Maxwell law can be grouped together since the equations are homogeneous, and be seen as geometric identities expressing the field F (a 2-form), which can be derived from the 4-potential A. Gauss's law for electricity and the Ampere–Maxwell law could be seen as the dynamical equations of motion of the fields, obtained via the Lagrangian principle of least action, from the "interaction term" AJ (introduced through gauge covariant derivatives), coupling the field to matter. For the field formulation of Maxwell's equations in terms of a principle of extremal action, see electromagnetic tensor.

Often, the time derivative in the Faraday–Maxwell equation motivates calling this equation "dynamical", which is somewhat misleading in the sense of the preceding analysis. This is rather an artifact of breaking relativistic covariance by choosing a preferred time direction. To have physical degrees of freedom propagated by these field equations, one must include a kinetic term for A, and take into account the non-physical degrees of freedom that can be removed by gauge transformation . See also gauge fixing and Faddeev–Popov ghosts.

This formulation uses the algebra that spacetime generates through the introduction of a distributive, associative (but not commutative) product called the geometric product. Elements and operations of the algebra can generally be associated with geometric meaning. The members of the algebra may be decomposed by grade (as in the formalism of differential forms) and the (geometric) product of a vector with a k-vector decomposes into a -vector and a -vector. The -vector component can be identified with the inner product and the -vector component with the outer product. It is of algebraic convenience that the geometric product is invertible, while the inner and outer products are not. As such, powerful techniques such as Green's functions can be used. The derivatives that appear in Maxwell's equations are vectors and electromagnetic fields are represented by the Faraday bivector F. This formulation is as general as that of differential forms for manifolds with a metric tensor, as then these are naturally identified with r-forms and there are corresponding operations. Maxwell's equations reduce to one equation in this formalism. This equation can be separated into parts as is done above for comparative reasons.

Ricci calculus Electromagnetic wave equation Speed of light Electric constant Magnetic constant Free space Near and far field Electromagnetic field Electromagnetic radiation Quantum electrodynamics List of electromagnetism equations

The source of the worked problems is Warnick and Russer, 2006.
