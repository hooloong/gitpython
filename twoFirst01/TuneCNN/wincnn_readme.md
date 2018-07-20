# Wincnn FAQ

### How do Winograd's fast convolution algorithms work?

In a nutshell, Winograd's fast convolution algorithms transform input and filters into another space where convolution becomes element-wise multiplication. The fourier transform also turns convolutions into element-wise multiplications, but uses complex numbers. Complex number multiplication requires 3 real multiplications, and hermitian symmetry in the discrete fourier transform (DFT) of real valued data effectively reduces this to about 1.5 multiplications per input. Winograd minimal algorithms only need 1 real multiplication per input, which is essentially the computational advantage that Winograd convolution has over DFT.

It is worth noting that while 3/2 = 1.5 real multiplications per complex multiplication is achieved in theory, 4/2 = 2 is used more often for FFT based CNN acceleration, because the former uses more workspace memory, which might outweight the benefits of reduced mutliplications.

Wincnn generates a subset of the Winograd convolution algorithms that are called modified Cook-Toom algorithms. These use the provably minimal number of multiplications for convolution. Wincnn uses the Lagrange Interpolating Polynomial to transform polynomial multiplication, which is equivalent to convolution, into element-wise multiplication of the values that the polynomials take at a fixed number of interpolation points. The down-side of Cook-Toom algorithms is that the transforms quickly become unstable as the transform size increases. However they are a good match for the small 3x3 convolutions used in convolutional neural networks.

The more general formulation of Winograd's fast convolution algorithms uses the Chinese Remainder Theorem. These algorithms include the Cook-Toom algorithms, but can also be used to generate algorithms that use more multiplications but have simpler transforms. See the [supplementary material](2464-supp.pdf) from the paper [Fast Algorithms for Convolutional Neural Networks](http://www.cv-foundation.org/openaccess/content_cvpr_2016/html/Lavin_Fast_Algorithms_for_CVPR_2016_paper.html) for an introduction to this technique.

Winograd convolution algorithms are a rich subject that has been documented extensively in digital signal processing literature. We encourage the enthusiastic reader to read the source material:

[1] Shmuel Winograd. Arithmetic complexity of computations, volume 33. Siam, 1980.
[2] Richard E Blahut. Fast algorithms for signal processing. Cambridge University Press, 2010.
[3] V. Madisetti. The Digital Signal Processing Handbook. Number v. 2 in Electrical engineering handbook series. CRC, 2010.
[4] Andrei L Toom. The complexity of a scheme of functional elements realizing the multiplication of integers. In Soviet Mathematics Doklady, volume 3, pages 714–716, 1963.
[5] SA Cook. On the minimum computation time for multiplication. Doctoral diss., Harvard U., Cambridge, Mass, 1966.

### What about all of those transform operations? Is the total number of arithmetic operations actually reduced?

Basically the number of multiply-accumulates in the multiplication stage dominates the number of arithmetic operations (additions, multiplications, or multiply-accumulates) in the transform stages, provided that the dimensions of the neural network layer are all large enough.

Example:
A 3x3 convolutional layer has C input channels and K output channels, and spatial dimensions HxW. The direct algorithm use HWCK9 multiply accumulates. F(4x4, 3x3) uses (H/4)(W/4)CK(36) = HWCK(2.25) multiply accumulates, in addition to (H/4)(W/4)C(144) arithmetic instructions for the data transform, CK(72) for the filter transform, and (H/4)(W/4)K(100) for the inverse transform.

So the reason the number of arithmetic instructions in the transforms do not matter is that the multiplication stage is O(HWCK) while the transforms are O(HWC), O(CK), and O(HWK), respectively. So each of the transforms is less by a factor of K, HW, or C. If all of these dimensions are large, then the amount of arithmetic in the transforms is dominated by the multiplication stage.

### Can Winograd fast convolution algorithms be used with strided convolutions?

It is possible to use Winograd or any convolution algorithm with strides > 1 by decimating the input and filter to make un-strided convolutions, then adding the results.

For example:
```
xoxoxoxoxox
*2
xox
=
xxxxxx * xx + ooooo * o
```

So a 1D stride 2 convolution can be decomposed into the sum of two un-strided convolutions, each using half of the data and filter elements. You can use a Winograd algorithm on each of the un-strided convolutions.

The same technique can be used with strided 2D convolutions, but then you need a sum of 4 un-strided convolutions.

Any book about fast digital signal processing algorithms will have a chapter on "Decimated Convolution" (ie strided convolution), but they usually only discuss the 1D case.

I probably first became aware of this technique from the following paper by Brosch and Tam, which does use 2D decimation in conjunction with FFT convolution: https://www.researchgate.net/profile/Tom_Brosch/publication/267930193_Efficient_Training_of_Convolutional_Deep_Belief_Networks_in_the_Frequency_Domain_for_Application_to_High-Resolution_2D_and_3D_Images/links/55f05f3d08ae0af8ee1d1904.pdf

### What about dilated convolutions?

In general, the Winograd algorithm or any fast convolution algorithm can be used with dilated convolution.

This is easily seen if we first consider that dilated convolution is really just convolution on a shifted, decimated input. That is, in order to compute a dilated convolution with scale 2<sup>i</sup>, you can first decimate the input signal X by removing all the rows and columns except for the ones at distance 2<sup>i</sup>, to give a decimated signal X<sub>i</sub>. You then perform regular convolution on X<sub>i</sub>.

You need to repeat this process for all shifts of the signal X by (j,k) pixels where (0,0) <= (j,k) < (2<sup>i</sup>, 2<sup>i</sup>). Call each of these decimated shifts X<sub>ijk</sub>, then the dilated convolution is the union of all the Y<sub>ijk</sub> = F * X<sub>ijk</sub>.

Now each of the F * X<sub>ijk</sub> is a regular convolution, so they each can be performed with a fast algorithm such as Winograd.


# wincnn

A simple python module for computing minimal Winograd convolution algorithms for use with
convolutional neural networks as proposed in [1].

Requirements

+ python: version 2.7.6
+ sympy: version 1.0 (0.7.4.1 does not work)

## Example: F(2,3)

For F(m,r) you must select m+r-2 polynomial interpolation points.

In this example we compute transforms for F(2,3) or
F(2x2,3x3) using polynomial interpolation points (0,1,-1).

```
andrew@broadwell:~/develop/wincnn$ python
Python 2.7.11+ (default, Apr 17 2016, 14:00:29)
[GCC 5.3.1 20160413] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import wincnn
>>> wincnn.showCookToomFilter((0,1,-1), 2, 3)
AT =
⎡1  1  1   0⎤
⎢           ⎥
⎣0  1  -1  1⎦

G =
⎡ 1    0     0 ⎤
⎢              ⎥
⎢1/2  1/2   1/2⎥
⎢              ⎥
⎢1/2  -1/2  1/2⎥
⎢              ⎥
⎣ 0    0     1 ⎦

BT =
⎡1  0   -1  0⎤
⎢            ⎥
⎢0  1   1   0⎥
⎢            ⎥
⎢0  -1  1   0⎥
⎢            ⎥
⎣0  -1  0   1⎦

AT*((G*g)(BT*d)) =
⎡d[0]⋅g[0] + d[1]⋅g[1] + d[2]⋅g[2]⎤
⎢                                 ⎥
⎣d[1]⋅g[0] + d[2]⋅g[1] + d[3]⋅g[2]⎦

```

The last matrix is the 1D convolution F(2,3) computed using the
transforms AT, G, and BT, on 4 element signal d[0..3] and 3 element
filter g[0..2], and serves to verify the correctness of the
transforms. This is a symbolic computation, so the result should be
exact.

## Example: F(4,3)

The following example computes transforms for F(4,3).

```
>>> wincnn.showCookToomFilter((0,1,-1,2,-2), 4, 3)
AT =
⎡1  1  1   1  1   0⎤
⎢                  ⎥
⎢0  1  -1  2  -2  0⎥
⎢                  ⎥
⎢0  1  1   4  4   0⎥
⎢                  ⎥
⎣0  1  -1  8  -8  1⎦

G =
⎡1/4     0     0  ⎤
⎢                 ⎥
⎢-1/6  -1/6   -1/6⎥
⎢                 ⎥
⎢-1/6   1/6   -1/6⎥
⎢                 ⎥
⎢1/24  1/12   1/6 ⎥
⎢                 ⎥
⎢1/24  -1/12  1/6 ⎥
⎢                 ⎥
⎣ 0      0     1  ⎦

BT =
⎡4  0   -5  0   1  0⎤
⎢                   ⎥
⎢0  -4  -4  1   1  0⎥
⎢                   ⎥
⎢0  4   -4  -1  1  0⎥
⎢                   ⎥
⎢0  -2  -1  2   1  0⎥
⎢                   ⎥
⎢0  2   -1  -2  1  0⎥
⎢                   ⎥
⎣0  4   0   -5  0  1⎦

AT*((G*g)(BT*d)) =
⎡d[0]⋅g[0] + d[1]⋅g[1] + d[2]⋅g[2]⎤
⎢                                 ⎥
⎢d[1]⋅g[0] + d[2]⋅g[1] + d[3]⋅g[2]⎥
⎢                                 ⎥
⎢d[2]⋅g[0] + d[3]⋅g[1] + d[4]⋅g[2]⎥
⎢                                 ⎥
⎣d[3]⋅g[0] + d[4]⋅g[1] + d[5]⋅g[2]⎦
```
## Linear Convolution

If instead of an FIR filter you want the algorithm for linear convolution, all you have to do is exchange and transpose the data and inverse transform matrices. This is referred to as the Transfomation Principle.

```
>>> wincnn.showCookToomConvolution((0,1,-1),2,3)
A =
⎡1  0 ⎤
⎢     ⎥
⎢1  1 ⎥
⎢     ⎥
⎢1  -1⎥
⎢     ⎥
⎣0  1 ⎦

G =
⎡ 1    0     0 ⎤
⎢              ⎥
⎢1/2  1/2   1/2⎥
⎢              ⎥
⎢1/2  -1/2  1/2⎥
⎢              ⎥
⎣ 0    0     1 ⎦

B =
⎡1   0  0   0 ⎤
⎢             ⎥
⎢0   1  -1  -1⎥
⎢             ⎥
⎢-1  1  1   0 ⎥
⎢             ⎥
⎣0   0  0   1 ⎦

Linear Convolution: B*((G*g)(A*d)) =
⎡      d[0]⋅g[0]      ⎤
⎢                     ⎥
⎢d[0]⋅g[1] + d[1]⋅g[0]⎥
⎢                     ⎥
⎢d[0]⋅g[2] + d[1]⋅g[1]⎥
⎢                     ⎥
⎣      d[1]⋅g[2]      ⎦
```

## Example: F(6,3)

This example computes transform for F(6,3). We will use fraction interpolation points 1/2
and -1/2, so we use sympy.Rational in order to keep the symbolic computation exact (using floating point values would make the derivation of the transforms subject to rounding error).

```
>>> from sympy import Rational
>>> wincnn.showCookToomFilter((0,1,-1,2,-2,Rational(1,2),-Rational(1,2)), 6, 3)
AT =
⎡1  1  1   1    1    1      1    0⎤
⎢                                 ⎥
⎢0  1  -1  2   -2   1/2   -1/2   0⎥
⎢                                 ⎥
⎢0  1  1   4    4   1/4    1/4   0⎥
⎢                                 ⎥
⎢0  1  -1  8   -8   1/8   -1/8   0⎥
⎢                                 ⎥
⎢0  1  1   16  16   1/16  1/16   0⎥
⎢                                 ⎥
⎣0  1  -1  32  -32  1/32  -1/32  1⎦

G =
⎡ 1      0     0  ⎤
⎢                 ⎥
⎢-2/9  -2/9   -2/9⎥
⎢                 ⎥
⎢-2/9   2/9   -2/9⎥
⎢                 ⎥
⎢1/90  1/45   2/45⎥
⎢                 ⎥
⎢1/90  -1/45  2/45⎥
⎢                 ⎥
⎢ 32    16        ⎥
⎢ ──    ──    8/45⎥
⎢ 45    45        ⎥
⎢                 ⎥
⎢ 32   -16        ⎥
⎢ ──   ────   8/45⎥
⎢ 45    45        ⎥
⎢                 ⎥
⎣ 0      0     1  ⎦

BT =
⎡1   0    -21/4    0    21/4     0    -1  0⎤
⎢                                          ⎥
⎢0   1      1    -17/4  -17/4    1    1   0⎥
⎢                                          ⎥
⎢0   -1     1    17/4   -17/4   -1    1   0⎥
⎢                                          ⎥
⎢0  1/2    1/4   -5/2   -5/4     2    1   0⎥
⎢                                          ⎥
⎢0  -1/2   1/4    5/2   -5/4    -2    1   0⎥
⎢                                          ⎥
⎢0   2      4    -5/2    -5     1/2   1   0⎥
⎢                                          ⎥
⎢0   -2     4     5/2    -5    -1/2   1   0⎥
⎢                                          ⎥
⎣0   -1     0    21/4     0    -21/4  0   1⎦

AT*((G*g)(BT*d)) =
⎡d[0]⋅g[0] + d[1]⋅g[1] + d[2]⋅g[2]⎤
⎢                                 ⎥
⎢d[1]⋅g[0] + d[2]⋅g[1] + d[3]⋅g[2]⎥
⎢                                 ⎥
⎢d[2]⋅g[0] + d[3]⋅g[1] + d[4]⋅g[2]⎥
⎢                                 ⎥
⎢d[3]⋅g[0] + d[4]⋅g[1] + d[5]⋅g[2]⎥
⎢                                 ⎥
⎢d[4]⋅g[0] + d[5]⋅g[1] + d[6]⋅g[2]⎥
⎢                                 ⎥
⎣d[5]⋅g[0] + d[6]⋅g[1] + d[7]⋅g[2]⎦
```

[1] "Fast Algorithms for Convolutional Neural Networks" Lavin and Gray, CVPR 2016.
http://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Lavin_Fast_Algorithms_for_CVPR_2016_paper.pdf
