# Homomorphic-Encryption

**1.Learning with Errors**

<br/>
We denote by Zq the set of integers (−q/2,q/2] where q > 1 is an integer, all integer operations will be performed mod q if not stated otherwise, and for simplicity, you will see me mostly deal with positive integers in [0,q), but keep in mind that it's the same as our Zq, as

−x ≡ q−x (mod q) where x is a positive integer (e.g. −1 ≡ 6 (mod7) ). An element v ∈ Zqⁿ would be simply a vector of n elements in Zq.

We will use [⋅]m to specify that we are applying modulo m, and ⌊⋅⌉ for rounding to the nearest integer. We denote by ⟨a,b⟩ the inner product of two elements a,b ∈ Zqn and is defined as follows

⟨a,b⟩ = ᵢΣⁿ aᵢ.bᵢ (mod q)


Learning With Error (LWE) was introduced
by Regev in 2009 and
can be defined as follows: For integers n≥1 and q≥2, let's consider the following
equations,



⟨s,a₁⟩ + e₁ = b₁ (mod q)

⟨s,a₂⟩ + e₂ = b₂ (mod q)

...

⟨s,aₘ⟩ + eₘ = bₘ (mod q)


where s and ai are chosen independently and uniformly
from Zqⁿ, and eᵢ are
chosen independently according to a probability distribution over Zq, and bᵢ ∈ Zq. The LWE problem state that it's hard to recover s from the pairs (aᵢ,bᵢ), and it's on such hardness that cryptography generally lies.

<br/>

**2.Key Generation**

<br/>
We start by generating a random secret-key sk from a probability distribution, we will use the uniform distribution over R₂, which means sk will be a polynomial with coefficients being 0 or 1. For the public-key we first sample a polynomial a uniformly over Rq and a small error polynomial e from a discrete normal distribution over Rq. We then set the public-key to be the tuple 

pk=([−(a⋅sk+e)]q,a).


<br/>

**3.Encryption**

<br/>
In our case we will want to encrypt integers in Zₜ so we will need to encode this integer into the plaintext domain Rₜ, we will simply encode an integer pₜ (for plaintext) as the constant array m = pₜ (e.g. m=5 will hold the value of 5), where t is plaintext modulus. The encryption algorithm takes a public-key pk ∈ Rq × Rq and a plaintext array m ∈ Rₜ and outputs a ciphertext ct ∈ Rq × Rq, which is a tuple of two arrays ct₀ and ct₁ and they are computed as follows:

ct₀ = [pk₀⋅u + e₁ + δ⋅m]q

ct₁=[pk₁⋅u + e₂]q

where u is sampled from the uniform distribution over R₂ (same as the secret-key), e₁ and e₂ are sampled from a discrete normal distribution over Rq (same as the error term in key-generation), and δ is the integer division of q over t.


<br/>

**4.Decryption**

<br/>
The first intuition behind decryption is that (pk₁⋅sk ≈ −pk0) which means that they sum-up to a really small array. Let's try computing [ct₀+ct₁⋅sk]q:

[ct₀+ct₁⋅sk]q =[pk₀⋅u+e₁+δ⋅m+(pk₁⋅u+e₂)⋅sk]q

[ct₀+ct₁⋅sk]q =[pk₀⋅u+e₁+δ⋅m+pk₁⋅sk⋅u+e₂⋅sk]q

We can expand our public-key terms

[ct₀+ct₁⋅sk]q =[−(a⋅sk+e)⋅u+e₁+δ⋅m+a⋅sk⋅u+e₂⋅sk]q

[ct₀+ct₁⋅sk]q =[−a⋅sk⋅u−e⋅u+e₁+δ⋅m+a⋅sk⋅u+e₂.sk]q

[ct₀+ct₁⋅sk]q =[δ⋅m−e⋅u+e₁+e₂⋅sk]q

So we ended up with the scaled message and some error terms, let's multiply by 1/δ

(1/δ).[ct0+ct1⋅sk]q =[m + (1/δ)⋅errors]q

Then round to the nearest integer and go back to Rt

[⌊(1/δ).[ct₀+ct₁⋅sk]q ⌉]t=[⌊[m + (1/δ)⋅errors]q⌉]t

We will decrypt to the correct value m if the rounding to the nearest integer don't get impacted by the error terms, which means that the error terms must be bounded by 1/2

(1/δ)⋅errors ≤ ½ ⇔ errors ≤ q/2t

So all those error terms must be bounded by q/2t for a correct decryption. The parameters q and t clearly impact the correctness of the decryption, however, they are not the unique one.


<br/>

**5.Evaluation-Addition**

<br/>
Let ct be a ciphertext encrypting a plaintext message m₁, it's good to recall the structure of our ciphertext

ct=([pk₀⋅u+e₁+δ⋅m₁]q,[pk₁⋅u+e₂]q)

adding a plaintext message m₂ means that we should end up with a

ct₀=[pk₀⋅u+e₁+δ⋅(m₁+m₂)]q

we will just need to scale our new plaintext m₂ by δ and add it to ct0.

add_plain(ct,m₂)=([ct₀+δ⋅m2]q,ct₁)

Let's see how the decryption will look like after the addition

[⌊(1/δ).[ct₀+ct₁⋅sk]q ⌉]t=[⌊[m₁+m₂+(1/δ)⋅(−e⋅u+e₁+e₂⋅sk)]q⌉]t

As you may have already noticed, this operation doesn't add any extra noise, thus we can perform as many plain additions as we want without noise penalty.


<br/>

**6.Evaluation-Multiplication**

<br/>
Let ct be a ciphertext encrypting a plaintext message m₁, and we want to multiply it with a plaintext message m₂, which means that we should end up with

ct₀=[pk₀⋅u+e+δ⋅m₁⋅m₂]q 

this might seem pretty obvious ... right? but this time it's not, multiplying ct₀ with m₂ will result in

ct₀⋅m₂=[pk₀⋅u⋅m₂+e₁⋅m2+δ.m₁.m₂]q

expanding the public-key terms in [ct₀+ct₁⋅sk]q reveals that it won't decrypt correctly.

[ct₀+ct₁⋅sk]q =[pk₀⋅u⋅m₂+e₁⋅m₂+δ.m₁.m₂+pk₁⋅sk⋅u+e₂⋅sk]q

[ct₀+ct₁⋅sk]q =[−(a⋅sk+e)⋅u⋅m₂+e₁⋅m₂+δ.m₁.m₂+a⋅sk⋅u+e₂⋅sk]q

[ct₀+ct₁⋅sk]q =[−a⋅sk⋅u⋅m₂−e⋅u⋅m₂+e₁⋅m₂+δ⋅m₁⋅m₂+a⋅sk⋅u+e₂⋅sk]q

The issue is that −a⋅sk⋅u⋅m₂ and a⋅sk⋅u won't cancel each other now, and that's a big value added to our actual message m₁⋅m₂ and decryption will clearly fail. For a correct decryption, we will also need to multiply ct₁ by m₂

mul_plain(ct,m₂)=([ct₀⋅m₂]q,[ct₁⋅m₂]q)

So that we end up with

[ct₀+ct₁⋅sk]q = [−a⋅sk⋅u⋅m₂−e⋅u⋅m₂+e₁⋅m₂+δ⋅m₁⋅m₂+a⋅sk⋅u⋅m₂+e₂⋅sk⋅m₂]q

[ct₀+ct₁⋅sk]q =[δ⋅m₁⋅m₂−e⋅u⋅m₂+e₁⋅m₂+e₂.sk⋅m₂]q

And the decryption circuit will result in

[⌊(1/δ).[ct₀+ct₁⋅sk]q ⌉]t = [⌊[m₁⋅m₂+1δ⋅(−e⋅u⋅m₂+e₁⋅m₂+e₂⋅sk⋅m₂)]q⌉]t

Compared to the plaintext addition, you can see here that our error terms got scaled up by our message m₂ which means that multiplying with big values might introduce some rounding errors during decryption.
