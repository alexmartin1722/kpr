# Nonuniform sampling

Nonuniform sampling is a branch of sampling theory involving results related to the Nyquist–Shannon sampling theorem. Nonuniform sampling is based on Lagrange interpolation and the relationship between itself and the (uniform) sampling theorem. Nonuniform sampling is a generalisation of the Whittaker–Shannon–Kotelnikov (WSK) sampling theorem.

The sampling theory of Shannon can be generalized for the case of nonuniform samples, that is, samples not taken equally spaced in time. The Shannon sampling theory for non-uniform sampling states that a band-limited signal can be perfectly reconstructed from its samples if the average sampling rate satisfies the Nyquist condition. Therefore, although uniformly spaced samples may result in easier reconstruction algorithms, it is not a necessary condition for perfect reconstruction.

The general theory for non-baseband and nonuniform samples was developed in 1967 by Henry Landau. He proved that the average sampling rate (uniform or otherwise) must be twice the occupied bandwidth of the signal, assuming it is a priori known what portion of the spectrum was occupied. In the late 1990s, this work was partially extended to cover signals for which the amount of occupied bandwidth was known, but the actual occupied portion of the spectrum was unknown. In the 2000s, a complete theory was developed (see the section Beyond Nyquist below) using compressed sensing. In particular, the theory, using signal processing language, is described in this 2009 paper. They show, among other things, that if the frequency locations are unknown, then it is necessary to sample at least at twice the Nyquist criteria; in other words, you must pay at least a factor of 2 for not knowing the location of the spectrum. Note that minimum sampling requirements do not necessarily guarantee numerical stability.

For a given function, it is possible to construct a polynomial of degree n which has the same value with the function at n + 1 points.
Interpolation using spline functions is one of the mathematical methods used.
Let the n + 1 points to be z_0, z_1, \ldots , z_n, and the n + 1 values to be w_0, w_1, \ldots, w_n.
In this way, there exists a unique polynomial p_n(z) such that
p_n(z_i) = w_i, \text{ where }i = 0, 1, \ldots, n.
Furthermore, it is possible to simplify the representation of p_n(z) using the interpolating polynomials of Lagrange interpolation:
I_k(z) = \frac{(z-z_0)(z-z_1)\cdots(z-z_{k-1})(z-z_{k+1})\cdots(z-z_n)}{(z_k-z_0)(z_k-z_1)\cdots(z_k-z_{k-1})(z_k-z_{k+1})\cdots(z_k-z_n)}
From the above equation:
I_k(z_j) = \delta_{k,j} = \begin{cases} 0, & \text{if }k\ne j \\ 1, & \text{if }k = j \end{cases}
As a result,
p_n(z) = \sum_{k=0}^n w_kI_k(z)
p_n(z_j) = w_j, j = 0, 1, \ldots, n
To make the polynomial form more useful:
G_n(z) = (z-z_0)(z-z_1)\cdots(z-z_n)
In that way, the Lagrange Interpolation Formula appears:
p_n(z) = \sum_{k=0}^n w_k\frac{G_n(z)}{(z-z_k)G'_n(z_k)}
Note that if f(z_j)=p_n(z_j), j=0, 1, \ldots, n,, then the above formula becomes:
f(z) = \sum_{k=0}^n f(z_k)\frac{G_n(z)}{(z-z_k)G'_n(z_k)}

Whittaker tried to extend the Lagrange Interpolation from polynomials to entire functions.
He showed that it is possible to construct the entire function
C_f(z) = \sum_{n=-\infty}^\infty f(a+nW)\frac{\sin[\pi(z-a-nW)/W]}{[\pi(z-a-nW)/W]}
which has the same value with f(z) at the points z_n = a + nW
Moreover, C_f(z) can be written in a similar form of the last equation in previous section:
C_f(z) = \sum_{n=-\infty}^{\infty}f(z_n)\frac{G(z)}{G'(z_n)(z-z_n)},\text{ where }G(z)=\sin[\pi(z-z_n)/W]\text{ and }z_n=a+nW
When a = 0 and W = 1, then the above equation becomes almost the same as WSK theorem:
If a function f can be represented in the form f(t) = \int_{-\sigma}^\sigma e^{jxt}g(x)\, dx \qquad (t\in \mathbb{R}), \qquad \forall g\in L^2(-\sigma,\sigma),
then f can be reconstructed from its samples as following:
f(t) = \sum_{k=-\infty}^\infty f\left(\frac{k\pi}{\sigma}\right)\frac{\sin(\sigma t-k\pi)}{\sigma t-k\pi} \qquad (t\in \mathbb{R})
The sampling theorem imposes conditions on sampling continuous signals.
These conditions are intended to prevent signal defects during reconstruction after sampling.
Sampling frequencies exceeding this limit result in aliasing.
Components with frequencies higher than the sampling rate are reconstructed as signals with lower frequencies.
This reconstruction results in distortion.
This type of distortion is called aliasing.
The original and reconstructed signals have identical sampled values.
During reconstruction, it is impossible to determine which specific signal component caused the distortion.
There are two ways to avoid aliasing.
One way is to increase the sampling frequency.
This approach ensures compliance with the Nyquist criterion.

For a sequence \{t_k\}_{k\in \mathbb{Z}} satisfying D=\sup_{k\in\mathbb{Z}}|t_k-k|<\frac{1}{4},
then f(t) = \sum_{k=-\infty}^\infty f(t_k)\frac{G(t)}{G'(t_k)(t-t_k)},\qquad \forall{}f\in B^2_\pi,\qquad (t\in \mathbb{R}), where \textstyle G(t)=(t-t_0)\prod_{k=1}^\infty \left(1-\frac{t}{t_k}\right)\left(1-\frac{t}{t_{-k}}\right), B^2_\sigma is Bernstein space, and f(t) is uniformly convergent on compact sets.
The above is called the Paley–Wiener–Levinson theorem, which generalize WSK sampling theorem from uniform samples to non uniform samples.
Both of them can reconstruct a band-limited signal from those samples, respectively.
The sampling has gaps.
Samples are taken from a judiciously chosen subset of points.
The actual gaps between measurements are significantly larger than the base spacing.
The most common implementation of non-uniform sampling anti-aliasing signal processing methods involves introducing a series of high-precision and known time intervals as the sampling spacing.
The average sampling rate is calculated by dividing the total number of sample points by the total sampling time.

== Applications and Motivation ==

In the context of digital signal processing, these methods are used with equipment that has limited sensor speed or spatial density to simulate a higher frequency or density signal sampling.
Mathematical methods, including filtering, are used to reconstruct the content of the gaps in data that can be reconstructed through appropriate filtering.
For quasi-periodic signals whose shape can evolve slowly over time and vary little between successive periods, the goal is to observe the signal on an oscilloscope when the available equipment cannot sample the signal because its sampling frequency is not higher than required by the sampling theorem.
The quasi-periodicity property of the signal can be utilized for sampling over a sufficiently long duration, yielding reasonably correct results.
The signal is not perfectly periodic, and this non-periodic nature prevents stable observation for a sufficiently long duration, which is required to reconstruct the signal perfectly.
Reconstruction can be performed using random sampling.

This method produces a reasonably probable estimate of the signal's appearance.
The same situation occurs in spectral methods within numerical analysis.

== Anti-aliasing Filters ==

A low-pass filter can be introduced to avoid aliasing, and this type of filter is commonly called an anti-aliasing filter.
The purpose of the filter is to remove signals higher than the maximum frequency.
Uniform sampling often includes more sample points than necessary, and the purpose of using extra sample points in uniform sampling is to prevent aliasing.

== References ==

Guy Binet is the author of the 2013 book Traitement numérique du signal.
