---
marp: true
math: mathjax
---

# SAT solver s grananjem po najkraćem termu (za latinske kvadrate)
## Pregled
Ovaj projekt prezentira rekurzivni KNF solver napisan u pythonu. Cilj nije maksimalna optimizacija nego predstavljanje ideje algoritma. Cijeli projekt se nalazi na mom github računu te je dostupan za skidanje.
`https://github.com/MrStark135/SAT-solver`

## Postavljanje
Postupak postavljanja je prikazan u `README.md` dokumentu, ovo je samo sažetak
```bash
git clone https://github.com/MrStark135/SAT-solver.git
cd sat-solver
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Riječnik pojmova 
- **Varijabla**: zapis je bilo koji string, npr. `A`, `BF`, `HR5`
- **Literal**: sama varijabla ili njezina negacija, npr. `A`, `~A`
- **Klauzula/Term**: disjunkcija literala, npr. `(A ∨ ~B ∨ C)`
- **CNF**: konjunkcija klauzula/termova
- **SAT/UNSAT**: označava je li zadanu KNF moguće zadovoljiti postavljanjem varijabli na određenu kombinaciju vrijednosti ili ne postoji kombinacija vrijednosti koja zadovoljava yadanu KNF

 
## Algoritam

### Osnovna ideja
Odaberi **najkraći term**, isprobaj svaku kombinaciju vrijednosti varijabli koja ju zadovoljava, pa **pojednostavi** ostatak formule evaluacijom zadanih vrijednosti i **rekurzivno ponovi**.
> Najkraći term ima najmanje mogućnosti → najmanji faktor grananja, bolja optimizacija

### Postupak

1. **Postavi varijable najkraćeg terma:** Term s $k$ literala istinit je za svaku kombinaciju osim one u kojoj su sve vrijednosti `False`:

	| k | kombinacije koje se isprobavaju | `2^k − 1` |
	|---|---|---|
	| 1 | `(T)` | 1 |
	| 2 | `(T,T) (T,F) (F,T)` | 3 |
	| 3 | sve osim `(F,F,F)` | 7 |

	Pritom je bitno napomenut, da literali mogu bit negirani, dakle uzimaju se vrijednosti za koje je cijeli term `True`, npr. `(T,F,F)` je kombinacija koja se ne uzima za term `(~A, B, C)`
2. **Redukcija KNF:** Za svaku od tih kombinacija se literali evaluiraju i KNF se reducira tako da: 
	- vrijednost literala je `True` - svaki term koji sadržava taj literal je automatski zadovoljen - disjunkcija je `True` ako je barem jedan literal `True`
	- vrijednost literala je `False` - taj literal se može eliminirati iz svih termova koji ga sadrže jer ne pridonosi istinitosti
3. **Rekurzija:** Reducirana KNF se uzima kao osnova te se rekurzivno ponavlja postupak sve dok:
	- **sve varijable su postavljene** - pronađena je kombinacija vrijednosti varijabli koja zadovoljava zadanu KNF
	- **ostane term koji nema više literala** - prazni term znači da su svi literali evaluirali `False` - a budući da za konjunkciju je dovoljan jedan term `False` da bude `False` - došlo je do **konflikta**. U tome slučaju rekurzivni postupak izlazi jedan nivo iznad te pokušava sa drugim kombinacijama sve dok se ne zadovolje svi termovi

## Kompleksnost izvršavanja
Brute-force pristup, najosnovniji, se temelji na prolaženju kroz sve moguće kombinacije zadanih vrijednosti ya sve varijable, dakle za $n$ varijabli imamo $2^n$ mogućnosti, i kompleksnost algoritma je $\mathcal{O}(2^n)$

Za ovaj algoritam kompleksnost je definirana duljinom "najkraćih termova", 
> problem: ne možemo unaprijed znati "sve najkraće" duljine

> problem: nisu sve klauzule jednake duljina i svakako prosječna duljina jako utječe na efikasnost algoritma

1. Recimo da je kompleksnost jednog problema $L(n)$

2. Jedan term postavlja $k$ varijabli te reducira problem na $(2^k-1)$ podproblema.
	 > jer postoji $2^k$ kombinacija a samo jedna od njih ne zadovoljava term

3. Dakle kompleksnost kad se primjeni rekurzija je $$L(n) = (2^k - 1)\cdot L(n-k)$$ kad se izraz razloži $$L(n)=(2^{k_1}-1)(2^{k_2}-1)\cdots(2^{k_d}-1)$$ ili sažetije $$\prod_{i=1}^{d}(2^{k_i}-1)$$
gdje je $d$ dubina rekurzije a $k_i$ su razne vrijednosti najkraćih termova. Isto tako znamo da $k_1+k_2+k_3...k_d =\sum_{i=1}^{d}k_i=n$ jer svaki term testira $k$ varijabli, dakle nakon svakog pojednostavljivanja KNF-a preostaje $n-k$, sve dok nema više varijabli za postaviti, tj. $n=0$

4. Efikasnost ovog algoritma, tj. smanjenje vrijednosti $\prod_{i=1}^{d}(2^{k_i}-1)$, raste za male vrijednosti $k_i$, dakle algoritam riješava brže KNF sa malim klauzulama, dok za veće vrijednosti $k_i$, $k_i \to n$ pa $d \to 1$ dakle $\prod_{i=1}^{d}(2^{k_i}-1) \approx 2^n-1$ - znači kompleksnost se približava brute-force kompleksnosti

5. Međutim, ovaj algoritam primjenjen na latinske kvadrate pokazuje jako dobre rezultate upravo zbog načina kako su zadana pravila u KNF-u, tj. većina termova sadrže 2 literala, što znači $k \to 2, d \to n/2$. Dakle optimizacija je: $$\prod_{i=1}^{d}(2^{k_i}-1) \approx \prod_{i=1}^{n/2}(2^2-1)=(\sqrt{3})^n$$ što u usporedbi sa brute-force kompleksnosću je primjetno bolje $2^n > 1.732^n$, no zbog eksponencijalnog rasta svejedno eksplodira nakon nekog vremena

 
## Ograničenja
- Dubina rekurzije max 1000, za najgori slučaj $d=n$ 1000 varijabli, no ne nužno strogi maksimum. Za latinske kvadrate to znači 10x10 kvadrat. Taj limit se može malo pomaknuti optimizacijom ili promjenom defaultne maksimalne rekurzije

- **Prazan CNF** `solve_sat([])` → `None` – solver vraća *pridruživanje* koje zadovoljava, a praznoj KNF se nema što pridružiti

- Ima dosta prostora za optimizaciju

- TODO: definiranje dodatnih pravila ya 9x9 sudoku?
 
