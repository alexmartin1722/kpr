# Claim proposal — Nonuniform sampling
*47 facts proposed for addition from non-English editions (fr, zh); 1 knowledge conflicts.*

## Proposed additions (ABSENT facts, routed to a section)

### Nonuniform sampling
- The sampling has gaps  
  _[fr]_ ← "- mais "avec des trous", et, en faisant des suppositions ou en utilisant des connaissances a-priori relatives aux propriétés du signal échantillonné, à utiliser…"
- Samples are taken from a judiciously chosen subset of points.  
  _[fr]_ ← "On peut néanmoins mettre à profit la propriété de quasi périodicité de ce signal pour en faire un échantillonnage raisonnablement correct en prenant sur une dur…"
- The actual gaps between measurements are significantly larger than the base spacing.  
  _[fr]_ ← "On peut néanmoins mettre à profit la propriété de quasi périodicité de ce signal pour en faire un échantillonnage raisonnablement correct en prenant sur une dur…"
- The most common implementation of non-uniform sampling anti-aliasing signal processing methods involves introducing a series of high-precision and known time intervals as the sampling spacing.  
  _[zh]_ ← "最常使用的非均勻採樣抗混疊訊號處理法的實作,是引入一串高精度且已知的時間長度,作為取樣的間隔。"
- The average sampling rate is calculated by dividing the total number of sample points by the total sampling time  
  _[zh]_ ← "平均取樣率是藉由總取樣點除以總取樣時間得到,最小取樣數則在均勻與否的取樣皆相同,均勻取樣則常常有超過數量的取樣點,目的同樣是為了防止混疊。"

### Lagrange (polynomial) interpolation
- Interpolation using spline functions is one of the mathematical methods used  
  _[fr]_ ← "- mais "avec des trous", et, en faisant des suppositions ou en utilisant des connaissances a-priori relatives aux propriétés du signal échantillonné, à utiliser…"

### Whittaker–Shannon–Kotelnikov (WSK) sampling theorem
- The sampling theorem imposes conditions on sampling continuous signals  
  _[zh]_ ← "取樣定理限制了在對連續訊號取樣時的條件,如奈奎斯特準則,以避免取樣後的重構時產生訊號缺陷。"
- These conditions are intended to prevent signal defects during reconstruction after sampling  
  _[zh]_ ← "取樣定理限制了在對連續訊號取樣時的條件,如奈奎斯特準則,以避免取樣後的重構時產生訊號缺陷。"
- Sampling frequencies exceeding this limit result in aliasing  
  _[zh]_ ← "奈奎斯特準則用取樣率限制了最大取樣頻率,若是超出這個頻率就會產生混疊。"
- Components with frequencies higher than the sampling rate are reconstructed as signals with lower frequencies  
  _[zh]_ ← "高於取樣頻率的成分將被重構成低於取樣頻率的訊號,因而導致重構失真,這樣的失真就稱為混疊,因為這兩個訊號有同樣的取樣值,重構時並不能主動判斷是哪一個成分訊號造成的。"
- This reconstruction results in distortion  
  _[zh]_ ← "高於取樣頻率的成分將被重構成低於取樣頻率的訊號,因而導致重構失真,這樣的失真就稱為混疊,因為這兩個訊號有同樣的取樣值,重構時並不能主動判斷是哪一個成分訊號造成的。"
- This type of distortion is called aliasing  
  _[zh]_ ← "高於取樣頻率的成分將被重構成低於取樣頻率的訊號,因而導致重構失真,這樣的失真就稱為混疊,因為這兩個訊號有同樣的取樣值,重構時並不能主動判斷是哪一個成分訊號造成的。"
- The original and reconstructed signals have identical sampled values  
  _[zh]_ ← "高於取樣頻率的成分將被重構成低於取樣頻率的訊號,因而導致重構失真,這樣的失真就稱為混疊,因為這兩個訊號有同樣的取樣值,重構時並不能主動判斷是哪一個成分訊號造成的。"
- During reconstruction, it is impossible to determine which specific signal component caused the distortion  
  _[zh]_ ← "高於取樣頻率的成分將被重構成低於取樣頻率的訊號,因而導致重構失真,這樣的失真就稱為混疊,因為這兩個訊號有同樣的取樣值,重構時並不能主動判斷是哪一個成分訊號造成的。"
- There are two ways to avoid aliasing  
  _[zh]_ ← "一般有兩個方式可以避免混疊的發生,一是提高取樣頻率,使之達到最凹訊號頻率的兩倍以上,意即使之符合奈奎斯特準則。"
- One way is to increase the sampling frequency  
  _[zh]_ ← "一般有兩個方式可以避免混疊的發生,一是提高取樣頻率,使之達到最凹訊號頻率的兩倍以上,意即使之符合奈奎斯特準則。"
- This approach ensures compliance with the Nyquist criterion  
  _[zh]_ ← "一般有兩個方式可以避免混疊的發生,一是提高取樣頻率,使之達到最凹訊號頻率的兩倍以上,意即使之符合奈奎斯特準則。"

### Applications and Motivation  *(new section)*
- The context is digital signal processing  
  _[fr]_ ← "En traitement numérique du signal, les méthodes d'échantillonnage non uniforme ou irrégulier visent à contourner les limites imposées par le théorème de l'échan…"
- These methods are used with equipment that has limited sensor speed or spatial density  
  _[fr]_ ← "En traitement numérique du signal, les méthodes d'échantillonnage non uniforme ou irrégulier visent à contourner les limites imposées par le théorème de l'échan…"
- The principle of these methods involves simulating a higher frequency or density signal sampling  
  _[fr]_ ← "Le principe de ces méthodes consiste à faire comme si on avait un échantillonnage du signal de fréquence ou de densité supérieure"
- Mathematical methods are used to reconstruct the content of the gaps  
  _[fr]_ ← "- mais "avec des trous", et, en faisant des suppositions ou en utilisant des connaissances a-priori relatives aux propriétés du signal échantillonné, à utiliser…"
- Filtering is one of the mathematical methods used  
  _[fr]_ ← "- mais "avec des trous", et, en faisant des suppositions ou en utilisant des connaissances a-priori relatives aux propriétés du signal échantillonné, à utiliser…"
- The signal is quasi-periodic  
  _[fr]_ ← "Supposons par exemple qu'on veuille observer sur un oscilloscope, la forme d'un signal quasi périodique (la forme du signal peut évoluer lentement, mais il vari…"
- The goal is to observe a signal on an oscilloscope  
  _[fr]_ ← "Supposons par exemple qu'on veuille observer sur un oscilloscope, la forme d'un signal quasi périodique (la forme du signal peut évoluer lentement, mais il vari…"
- The signal's shape can evolve slowly over time  
  _[fr]_ ← "Supposons par exemple qu'on veuille observer sur un oscilloscope, la forme d'un signal quasi périodique (la forme du signal peut évoluer lentement, mais il vari…"
- The signal varies little between successive periods  
  _[fr]_ ← "Supposons par exemple qu'on veuille observer sur un oscilloscope, la forme d'un signal quasi périodique (la forme du signal peut évoluer lentement, mais il vari…"
- The available equipment cannot sample the signal  
  _[fr]_ ← "et qu'on ne dispose pas d'un équipement capable de l'échantillonner à une fréquence supérieure à comme le voudrait le théorème de l'échantillonnage."
- The sampling frequency of the available equipment is not higher than required by the sampling theorem  
  _[fr]_ ← "et qu'on ne dispose pas d'un équipement capable de l'échantillonner à une fréquence supérieure à comme le voudrait le théorème de l'échantillonnage."
- The quasi-periodicity property of the signal can be utilized for sampling.  
  _[fr]_ ← "On peut néanmoins mettre à profit la propriété de quasi périodicité de ce signal pour en faire un échantillonnage raisonnablement correct en prenant sur une dur…"
- This sampling method yields reasonably correct results.  
  _[fr]_ ← "On peut néanmoins mettre à profit la propriété de quasi périodicité de ce signal pour en faire un échantillonnage raisonnablement correct en prenant sur une dur…"
- The sampling is performed over a sufficiently long duration.  
  _[fr]_ ← "On peut néanmoins mettre à profit la propriété de quasi périodicité de ce signal pour en faire un échantillonnage raisonnablement correct en prenant sur une dur…"
- The data with gaps can be reconstructed  
  _[fr]_ ← "On aurait donc un échantillonnage à "avec des trous" qu'on va pouvoir reconstruire via un filtrage adéquat."
- Reconstruction is achieved through appropriate filtering  
  _[fr]_ ← "On aurait donc un échantillonnage à "avec des trous" qu'on va pouvoir reconstruire via un filtrage adéquat."
- The signal is not perfectly periodic  
  _[fr]_ ← "Dans cet exemple, le fait que le signal ne soit pas parfaitement périodique interdit de l'observer de façon stable pendant une durée suffisamment longue pour le…"
- The non-periodic nature of the signal prevents stable observation for a sufficiently long duration  
  _[fr]_ ← "Dans cet exemple, le fait que le signal ne soit pas parfaitement périodique interdit de l'observer de façon stable pendant une durée suffisamment longue pour le…"
- Stable observation for a sufficiently long duration is required to reconstruct the signal perfectly  
  _[fr]_ ← "Dans cet exemple, le fait que le signal ne soit pas parfaitement périodique interdit de l'observer de façon stable pendant une durée suffisamment longue pour le…"
- Reconstruction can be performed using random sampling  
  _[fr]_ ← "Cependant, la reconstruction à partir d'un échantillonnage aléatoire permet de produire une estimation raisonnablement probable de l'apparence du signal."
- This method produces a reasonably probable estimate of the signal's appearance  
  _[fr]_ ← "Cependant, la reconstruction à partir d'un échantillonnage aléatoire permet de produire une estimation raisonnablement probable de l'apparence du signal."
- The same situation occurs in spectral methods within numerical analysis.  
  _[zh]_ ← "同樣的狀況也出現在數值分析裡的頻譜法。"

### Anti-aliasing Filters  *(new section)*
- A low-pass filter can be introduced to avoid aliasing  
  _[zh]_ ← "二是引入低通濾波器,通常稱為抗混疊濾波器,用以濾除高於最大頻率之訊號。"
- This type of filter is commonly called an anti-aliasing filter  
  _[zh]_ ← "二是引入低通濾波器,通常稱為抗混疊濾波器,用以濾除高於最大頻率之訊號。"
- The purpose of the filter is to remove signals higher than the maximum frequency  
  _[zh]_ ← "二是引入低通濾波器,通常稱為抗混疊濾波器,用以濾除高於最大頻率之訊號。"
- Uniform sampling often includes more sample points than necessary  
  _[zh]_ ← "平均取樣率是藉由總取樣點除以總取樣時間得到,最小取樣數則在均勻與否的取樣皆相同,均勻取樣則常常有超過數量的取樣點,目的同樣是為了防止混疊。"
- The purpose of using extra sample points in uniform sampling is to prevent aliasing  
  _[zh]_ ← "平均取樣率是藉由總取樣點除以總取樣時間得到,最小取樣數則在均勻與否的取樣皆相同,均勻取樣則常常有超過數量的取樣點,目的同樣是為了防止混疊。"

### References  *(new section)*
- Guy Binet is the author  
  _[fr]_ ← "Guy Binet: Traitement numérique du signal"
- The title of the work is Traitement numérique du signal  
  _[fr]_ ← "Guy Binet: Traitement numérique du signal"
- The book was published in 2013  
  _[fr]_ ← "Ellipses, 2013."

## Knowledge conflicts (CONTRADICTED — human adjudication queue)

- **Non-English claim** _[fr]_: Non-uniform or irregular sampling methods aim to bypass the limits imposed by the Shannon sampling theorem
  - English says: Nonuniform sampling is a generalisation of the Whittaker–Shannon–Kotelnikov (WSK) sampling theorem.
  - Proposed reconciliation: 2023-08-07T02:04:23Z
