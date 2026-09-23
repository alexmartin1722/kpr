# Document diff — Content similarity detection
*Sentence-level diff, original English → after the KPR merge. 316 lines added/changed.*

```diff
--- Content_similarity_detection (original English)
+++ Content_similarity_detection (after KPR merge)
@@ -9,4 +9,45 @@
 
+== Motivations and scope ==
+
+The purpose of these processes is to identify cases of intellectual theft.
+Scientific plagiarism detection refers to a set of methods, and using these methods leads to the discovery of intellectual theft or scientific plagiarism.
+The majority of the scientific community recognizes that committing theft is highly inappropriate for those who consider themselves scholars.
+Committing scientific theft endangers the reputation of the individual scholar and the scientific community.
+There is a common but incorrect definition of academic success, according to which an academic is considered successful if they publish more articles or authored books.
+Some academics seek shortcuts to advance their careers and are sometimes attracted to methods such as publishing articles by any means possible or translating books and publishing them as original works.
+There is a strong motivation for scientific plagiarism in many countries, and academic plagiarism has increased significantly.
+These software programs were developed to combat this growing phenomenon.
+Works include designs such as images or videos.
+Plagiarism exists in journalism, literature, art, and architecture.
+Examples of such documents include academic publications, papers, books, reports, and applications.
+Most plagiarism cases are found in academia.
+
 Computer-assisted plagiarism detection (CaPD) is an Information retrieval (IR) task supported by specialized IR systems, which is referred to as a plagiarism detection system (PDS) or document similarity detection system.
+The task is computer plagiarism detection.
+The system compares the originality of text in digital form.
+The comparison checks if the text has been presented previously in other contexts.
+Only documents in digital format can be compared.
+The comparison is made against other documents and materials in digital format.
+The comparison is typically performed in three areas.
+One area is open Internet pages.
+Another area is databases and materials negotiated by the system itself with different publishers.
+The third area is files stored within the system.
+The system displays matches between the original text and other sources.
+The system generally displays these matches as percentage similarities.
+These systems modify search engine systems.
+The suspected document is referred to as the input document.
+The system determines a similarity threshold for two documents to be considered plagiarized.
+Computer-assisted detection allows for the comparison of vast collections of documents.
 A 2019 systematic literature review presents an overview of state-of-the-art plagiarism detection methods.
+
+== Manual detection ==
+
+The first solution to detect potential school plagiarism is to search for keywords or key phrases on a search engine, a method that is effective when a student has completely copied an article found on the Internet.
+Manual plagiarism detection requires good memory skills and excellent memory.
+There are many documents to compare in manual plagiarism detection, making the process impractical when too many documents need to be compared or when original documents are not available for comparison.
+
+== Types of plagiarism ==
+
+Literal copies are also known as flagrant copyright violations and can include cases of modestly disguised plagiarism.
+Plagiarism is defined as documents composed of mixed text segments from multiple sources.
 
@@ -25,2 +66,11 @@
 The researchers expected to find lower rates in group one but found roughly the same rates of plagiarism in both groups.
+Academic plagiarism is particularly prevalent in higher education.
+Plagiarism detection systems have been adopted in Finnish universities during the 2000s.
+Highly similar papers were further analyzed manually.
+The Deja Vu project used eTBLAST to detect highly similar papers.
+The database contained 70,000 pairs of paper data from around the world.
+The database focused on life sciences.
+Access to the database was free.
+Heliotext manages the website.
+The website was closed as of March 2, 2016.
 
@@ -29,2 +79,6 @@
 Global similarity assessment approaches use the characteristics taken from larger parts of the text or the document as a whole to compute similarity, while local methods only examine pre-selected text segments as input.
+Word-linking procedures can achieve good performance.
+An example of a lossless document model is parse trees.
+Another class of techniques for automatic plagiarism detection uses distance calculation algorithms.
+These algorithms originate from bioinformatics pattern comparisons.
 
@@ -35,3 +89,9 @@
 Minutiae matching with those of other documents indicate shared text segments and suggest potential plagiarism if they exceed a chosen similarity threshold.
+Documents with high fingerprint similarity are displayed as candidate source documents.
 Computational resources and time are limiting factors to fingerprinting, which is why this method typically only compares a subset of minutiae to speed up the computation and allow for checks in very large collection, such as the Internet.
+The use of document fingerprints offers advantages.
+Shingles are used for text verification.
+The system allows changing the length of shingles.
+The system allows changing the step (interval) of shingles.
+The number of overlapping words in shingles can be specified.
 
@@ -39,2 +99,3 @@
 When applied to the problem of plagiarism detection, documents are compared for verbatim text overlaps.
+Document verification by exact text overlap is a classic string comparison.
 Numerous methods have been proposed to tackle this task, of which some have been adapted to external plagiarism detection.
@@ -43,4 +104,10 @@
 Nonetheless, substring matching remains computationally expensive, which makes it a non-viable solution for checking large collections of documents.
-
-Bag of words analysis represents the adoption of vector space retrieval, a traditional IR concept, to the domain of content similarity detection.
+The average runtime of the substring matching algorithm is 2 hours per comparison.
+The Rabin-Karp algorithm enables searching for a text string within a text.
+The search is performed using a hash function.
+One of the main applications of the Rabin-Karp algorithm is plagiarism detection.
+The method involves comparing files character by character.
+
+Bag of words analysis represents the adoption of vector space retrieval, a traditional IR concept, to the domain of content similarity detection and is used in natural language processing.
+In this model, text is represented as an unordered set of words.
 Documents are represented as one or multiple vectors, e.g. for different document parts, which are used for pair wise similarity computations.
@@ -56,4 +123,11 @@
 Factors, including the absolute number or relative fraction of shared citations in the pattern, as well as the probability that citations co-occur in a document are also considered to quantify the patterns' degree of similarity.
+If an English document is cited within a multilingual paper, plagiarism may be inferred from that citation array.
+CitePlag applies to all fields of study.
+Citation identifies common quotes between two scientific works.
+Proximity of quotes in the text is a main criterion for defining a quote template.
+The degree of similarity between the document being checked and cited literature is a criterion for this technique.
+The proximity of the document being checked to the cited literature is a criterion for this technique.
 
 Stylometry subsumes statistical methods for quantifying an author's unique writing style and is mainly used for authorship attribution or intrinsic plagiarism detection.
+Stylometry is used to identify the authorship of anonymous documents.
 Detecting plagiarism by authorship attribution requires checking whether the writing style of the suspicious document, which is written supposedly by a certain author, matches with that of a corpus of documents written by the same author.
@@ -61,3 +135,10 @@
 This is performed by constructing and comparing stylometric models for different text segments of the suspicious document, and passages that are stylistically different from others are marked as potentially plagiarized/infringed.
+Texts from different sources will have different style models.
 Although they are simple to extract, character n-grams are proven to be among the best stylometric features for intrinsic plagiarism detection.
+The analysis is based on sequences of parts of speech.
+Various sequences of parts of speech are used as parameters for splitting.
+The algorithm extracts heterogeneous fragments from the text.
+These fragments have different frequencies of occurrence of the selected part-of-speech sequence.
+This indicates possible plagiarism at that location.
+Severe text reorganization can result in a style different from the source material.
 
@@ -67,2 +148,7 @@
 Paraphrase detection particularly benefits from highly parameterized pre-trained models.
+Modern artificial intelligence (AI) systems are successfully used in the fight against plagiarism.
+These AI systems demonstrate high efficiency compared to traditional methods.
+One of the key advantages of using AI-based plagiarism detection tools is that they check text for plagiarism based on images.
+Checking the target document using this method requires sufficient computing resources and capacity.
+These resources are necessary to efficiently perform pairwise comparisons between all reference documents.
 
@@ -71,3 +157,3 @@
 It is therefore symptomatic that detection accuracy decreases the more plagiarism cases are obfuscated.
-
+Plagiarism detection is an actively studied engineering and scientific problem.
 Literal copies, a.k.a. copy and paste (c&p) plagiarism or blatant copyright infringement, or modestly disguised plagiarism cases can be detected with high accuracy by current external PDS if the source is accessible to the software.
@@ -76,3 +162,2 @@
 By applying flexible chunking and selection strategies, they are better capable of detecting moderate forms of disguised plagiarism when compared to substring matching procedures.
-
 Intrinsic plagiarism detection using stylometry can overcome the boundaries of textual similarity to some extent by comparing linguistic similarity.
@@ -81,6 +166,6 @@
 The results of the International Competitions on Plagiarism Detection held in 2009, 2010 and 2011, as well as experiments performed by Stein, indicate that stylometric analysis seems to work reliably only for document lengths of several thousand or tens of thousands of words, which limits the applicability of the method to CaPD settings.
-
+These competitions are organized under the PAN initiative.
+The first plagiarism detection competition for Russian-language documents took place in 2017.
 An increasing amount of research is performed on methods and systems capable of detecting translated plagiarism.
 Currently, cross-language plagiarism detection (CLPD) is not viewed as a mature technology and respective systems have not been able to achieve satisfying detection results in practice.
-
 Citation-based plagiarism detection using citation pattern analysis is capable of identifying stronger paraphrases and translations with higher success rates when compared to other detection approaches, because it is independent of textual characteristics.
@@ -88,2 +173,4 @@
 It remains inferior to text-based approaches in detecting shorter plagiarized passages, which are typical for cases of copy-and-paste or shake-and-paste plagiarism; the latter refers to mixing slightly altered fragments from different sources.
+The more matching fragments found, the higher the likelihood of plagiarism.
+If a text contains mixed plagiarism from many sources, the accuracy of the detection system will decrease.
 
@@ -94,9 +181,156 @@
 
+== AT Blast and the Déjà vu database ==
+
+One of the efforts is a software named AT Blast, which is capable of identifying and discovering similar articles.
+One achievement of using this software is the creation of a medical article database, and the software was used to create a database of medical articles.
+The database is named Déjà vu, and medical articles are archived in a centralized system called Medline.
+Within this system, there were 18 million records available, and 75,000 articles appeared to be similar to each other.
+Additionally, 181 articles were identified as scientific plagiarism.
+The analysis identified 22 repeat offenders of scientific theft who came from ten different countries.
+Each offender committed the act between two and ten times.
+
+== Persian language detection systems ==
+
+There are currently several systems active for detecting text similarity in Persian, including Simin Noor, Hametajo, and Honamjo.
+Simin Noor was the first system to perform text similarity matching for the Persian language and uses data from Noormags and Noorlib.
+The collection covers the fields of humanities and Islamic sciences, but the system does not have sufficient supporting resources for technical fields.
+Hemetajo was developed to detect scientific plagiarism in articles written in Persian by the Information and Communication Technology Research Institute of Jihad University.
+The system covers various scientific fields including engineering, medicine, and humanities and uses artificial intelligence algorithms to perform the plagiarism detection process.
+Honamjo focuses on thesis comparison and can be used to check theses.
+The Homadjo system is developed by the Iranian Research Institute for Information Science and Technology (IranDoc), and the use of this system is currently limited to universities and professors.
+
+== Finnish detection systems ==
+
+Urkund, Turnitin, and Ephrous are systems used in Finland.
+The University of Technology in Tampere developed a plagiarism detection system called Nalkki between 2008 and 2009.
+Nalkki is an open-source software.
+
+== General software capabilities and formats ==
+
+Several software programs with substantially identical features have appeared recently.
+These tools range from simple document comparison to advanced systems that can automatically search for sources from the Internet.
+Depending on their level of maturity, the software can process a varying number of file formats, with Word, PDF, and HTML files being among the most common.
+One type of software operates on a remote server, while some can be installed directly on the user's machine.
+The first type is generally the most effective.
+
+== French language detection tools ==
+
+Plag.fr is a plagiarism detection tool that detects plagiarism in the French language and offers both free and advanced paid options.
+Plagramme is a free plagiarism detection tool that detects plagiarism in French language text and offers advanced paid options.
+
+== General online and web-based tools ==
+
+Plagiarismhunt.com is a plagiarism checker that offers multi-checker options.
+The online plagiarism checker provides a similarity percentage and sources.
+PLText developed a plagiarism checker and a plagiarism remover tool, which was the world's first plagiarism checker and remover tool.
+3YA is a website that allows users to search for text on Google, Google Books, and Google Scholar.
+Baldr is a plagiarism detection tool.
+Plagium is a plagiarism detection tool that offers free plagiarism detection, paid advanced options, and a timeline of plagiarisms for news articles.
+WcopyFind was developed by a physics teacher.
+AntiPlag is a plagiarism search tool that offers free plagiarism search and provides automatic plagiarism detection.
+
+AntiPlag provides instant plagiarism detection.
+Scribbr offers a plagiarism detector.
+PlagScan compares with a database, compares with search engines, and provides an indication of the plagiarism level.
+Pompotron.com is intended for use by students.
+PRINCIX is a suite of tools designed for plagiarism detection that perform text similarity comparison.
+Compilatio offers plagiarism prevention and detection solutions for teachers, students, and writing professionals.
+The software can be used on the web.
+Copyleaks is a tool developed by Ankur that can detect plagiarism on the internet, search through document collections, analyze past reports, and compare specified reports against each other.
+
+Turnitin is an online tool developed by iParadigms, a US company, that detects plagiarism and improper citations in student reports and papers.
+The tools support English and Japanese.
+CrossCheck is a plagiarism detection tool developed by iParadigms and intended for publishers.
+Attributor, Copyscape, PlagScan, PlagTracker, and The Plagiarism Checker are plagiarism detection tools. [21,36,37,38] WriteCheck is a product of iParadigms, Inc. [21,36,37,38] Unplag.com and CopyMonitor are plagiarism detection services. [21,36,37,38] Lou Bloomfield provides software and websites for detecting plagiarism. [51,52]
+
+== iParadigms suite and specialized services ==
+
+iThenticate is a paid service developed by the US company iParadigms and is targeted at researchers and publishers.
+
+== File format support and limitations ==
+
+Plagium SeeSources WCopyfind detects similarity between specific file types, including .docx, .doc, .txt, .htm, .html, and .pdf.
+Plagium SeeSources WCopyfind cannot detect similarity with documents on the web or the internet.
+Plagium applies to English, multilingual texts, and all fields of study.
+WCopyfind applies to English, multilingual texts, and all fields of study.
+
+== Commercial and proprietary systems ==
+
+CopyTracker has closed source code.
+Chimpsky is a free plagiarism checker.
+Attributor, Copyscape, Ithenticate, Turnitin, Plagiarismdetect, PlagScan, and Veriguid are commercial plagiarism detection tools.
+Copyscape is a free tool for automatic plagiarism detection.
+PlagiatCheck is a free service for automatic plagiarism detection.
+Fairshare is a free service intended for bloggers and newspaper articles with RSS feeds.
+ETBLAST is a free tool for searching research articles in certain disciplines.
+Ephorus is a Dutch product.
+GenuineText and Urkund are Swedish products.
+Princix is a Swiss product.
+
+== Russian and Eastern European services ==
+
+Services in this category include Antiplagiat, Advego Plagiatus, Unicheck, miratools.ru, Praide Unique Content Analyser II, Plagiatinform, and Copyscape.
+The Antiplagiat system was developed by the company Forexsys.
+This system performs an online search, searches partner databases including the Russian State Library, the Scientific Electronic Library ELibrary.ru, and the company Lexpro, and searches the user's personal database.
+The Antiplagiat system performs searches on the Internet using its own means.
+The system has a free version in which only an abbreviated report format is available.
+Advego Plagiatus is a program that performs an online check using search engines.
+
+Advego Plagiatus does not use Yandex, allows users to make automatic search queries to Yandex, allows users to publish the search results on their own resources, displays the found sources, outputs a text match percentage, and does not convert letters.
+Miratools is a service with the website www.miratools.ru that allows for online text plagiarism checking [cite: 60], uses search engine results, provides a percentage of matches after the check [cite: 61,62], and identifies the sources found [cite: 61,62].
+Plagiatinform is a system that checks documents for plagiarism [cite: 65], searches within a local database [cite: 65], searches the Internet [cite: 65], can perform a quick search, can perform an in-depth search, provides verification results in the form of a report, and produces a report that is visual or easy to understand.
+
+Antiplagiat and Dissernet are tools.
+The system does not perform letter case conversion.
+The system cannot be used freely.
+The system cannot be tested freely.
+
+== Unplag and learning management integrations ==
+
+Unplag is a service and a tool that functions as a plagiarism detection service.
+It can perform plagiarism checks in real-time online and compare a document with a saved library of documents.
+Unplag offers a personal version and a corporate version.
+The service works with the Moodle, Canvas, Blackboard, and Sakai course management systems.
+
+== Istio and Praide features ==
+
+Istio is a service available at www.istio.com that checks text for borrowed content using search engines, including Yandex, to issue a message indicating whether the text is unique and to provide a list of similar website pages.
+The service provides additional tools for text analysis, including a spelling check and a tool that analyzes the most frequent words.
+Praide is a program also called Unique Content Analyser II that uses search engines to check texts.
+The program includes tools for adding new search engines and allows users to select the search engines to be used.
+A detailed report is generated for the check that covers each search engine used.
+The program does not support letter substitution, does not process stop words, and does not support working with a custom database.
+
+== Copyscape functionality and pricing ==
+
+Copyscape is a service that allows searching for copies of web pages on the Internet and returns a list of web pages containing text similar in content.
+The service checks for plagiarized content using the Google and Yahoo! search engines, checking only the content of the web page.
+To determine text uniqueness, the text must be published on a website and the system address of the page must be entered.
+There is a limit on the number of checks per month without registration and a limit on the number of displayed results without registration, which is 10 websites.
+There are no limits on the number of checks for registered users and no limits on the number of displayed results for registered users.
+Each request costs 5 cents.
+
+== General detection methods and sources ==
+
+CopyTracker is not a web-based system.
+Such a tool uses information published on the Internet to check if research articles, web pages, blog posts, student papers, or magazine articles contain quoted text.
+The local database contains saved student papers.
+Some systems compare text with scanned books on Google Books or with full-text versions of research articles, for which Google Scholar is an example of a source.
+
+== Regional products and integrations ==
+
+PlagScan is a German product.
+TurnitIn is an add-on for the North American learning platforms Blackboard and WebCT.
+
 Plagiarism in computer source code is also frequent, and requires different tools than those used for text comparisons in document.
 Significant research has been dedicated to academic source-code plagiarism.
-
+Baldr detects plagiarism in computer codes and programs.
+AI-based plagiarism detection tools can track plagiarism even in source code.
 A distinctive aspect of source-code plagiarism is that there are no essay mills, such as can be found in traditional plagiarism.
 Since most programming assignments expect students to write programs with very specific requirements, it is very difficult to find existing programs that already meet them.
+Programs found online may only meet some of the requirements.
+Meeting assignment requirements often requires rewriting or integrating programs.
+Rewriting or integrating programs is usually more difficult than learning programming for assignments independently.
 Since integrating external code is often harder than writing it from scratch, most plagiarizing students choose to do so from their peers.
-
+Most students plagiarize code assignments.
 According to Roy and Cordy, source-code similarity detection algorithms can be classified as based on either Strings – look for exact textual matches of segments, for instance five-word runs.
@@ -113,3 +347,2 @@
 Hybrid approaches – for instance, parse trees + suffix trees can combine the detection capability of parse trees with the speed afforded by suffix trees, a type of string-matching data structure.
-
 The previous classification was developed for code refactoring, and not for academic plagiarism detection (an important goal of refactoring is to avoid duplicate code, referred to as code clones in the literature).
@@ -117,2 +350,55 @@
 In an academic setting, when all students are expected to code to the same specifications, functionally equivalent code (with high-level similarity) is entirely expected, and only low-level similarity is considered as proof of cheating.
+
+== Detection resources and communities ==
+
+There are many blogs dedicated to detecting plagiarism, and these blogs also pursue individuals who commit plagiarism.
+Many of these blogs do not explicitly state their methods.
+Some resources are available in English only, some are available in Japanese only, and some support both languages.
+An example of a specific field is life sciences, while there are also resources that are not limited to any specific field.
+An online tool for checking the similarity of research results and publications with existing public information was released in Japan on August 28, 2013.
+There is a database of researcher incidents in Japan that is not public.
+Plagiarism cases have been discovered in the Japanese academic community, with 36 cases discovered between 1874 and 2009 and 23 cases discovered between 2000 and 2009.
+The website also pursues plagiarists, though the detection method is not explicitly stated.
+The items not marked with a circle include fabrication and alteration, and these items are not specialized in detecting plagiarism.
+The blog is named 'World Change Outlook'.
+
+The blog '11jigen' focuses on exposing fraudulent academic papers and covers research misconduct in general, including plagiarism, within the fields of Japanese language and life sciences.
+The operator of the blog is anonymous, and its activities were suspended after May 15, 2015, a status that is current as of March 2, 2016.
+PubPeer is a post-publication peer review site that operates in English and was active anonymously before switching to operating under its real name on August 31, 2015.
+The organizer of PubPeer was thought to be American but was actually a French person living in Paris.
+Retraction Watch is a website that monitors paper retractions.
+Vroniplag Wiki is a German-language website for accusing plagiarism, and Dissernet is a Russian-language website for accusing plagiarism.
+There is a blog titled 'Plagiarism and Research Misconduct' that is operated by Debora Weber-Wulff.
+
+Debora Weber-Wulff is affiliated with the Berlin University of Applied Sciences (Hochschule fur Technik und Wirtschaft Berlin).
+Lou Bloomfield is a physics professor at the University of Virginia in the United States and created the Plagiarism Resource Site.
+
+== Databases and tools ==
+
+Déjà Vu is a database used in scientific literature and is part of an open project.
+
+== Publications and competitions ==
+
+J.
+Carroll published a handbook for deterring plagiarism in higher education in 2002 in Oxford, associated with Oxford Brookes University.
+B.
+Zeidman wrote a 480-page book published in 2011.
+A competition was held under the framework of the 'Dialog' conference on computer linguistics.
+
+== MOSS ==
+
+Moss supports source code written in C, C++, Java, Pascal, Ada, ML, Lisp, Scheme, Perl, Python, Matlab, and Prolog.
+The tool is free to use.
+Developed in 1994 by Alex Aiken, a professor at the University of California, Berkeley, the system is operated by Stanford University in the United States and managed by Aiken.
+The system uses a plugin-based method.
+
+== JPlag ==
+
+JPlag is operated by the Karlsruhe Institute of Technology in Germany.
+JPlag can be used for free and requires registration.
+JPlag supports source code written in Java, C#, C, C++, and Scheme, as well as natural language text.
+
+== Program Dependence Graphs ==
+
+Program Dependence Graphs (PDG) represent the relationships between function calls within a program.
 
@@ -122,5 +408,25 @@
 The issue has been raised in a number of court cases.
-
+The software Turnitin was the subject of a scandal.
+Turnitin was accused of violating students' copyright.
+Students had their reports reused for commercial purposes by the software publisher.
+According to quotation law, very long quotations can constitute copyright infringement.
 An additional complication with the use of TMS is that the software finds only precise matches to other text.
 It does not pick up poorly paraphrased work, for example, or the practice of plagiarizing by use of sufficient word substitutions to elude detection software, which is known as rogeting.
+Text-matching software does not check for plagiarism sentence by sentence.
+The rate of false positives for software metrics is very high.
+To visually check if an author of a scientific paper is trying to trick the system, attention should be paid to the use of different font types and sizes.
+To visually check if an author of a scientific paper is trying to trick the system, attention should be paid to the use of fake links.
+To visually check if an author of a scientific paper is trying to trick the system, attention should be paid to the use of outdated facts.
+To visually check if an author of a scientific paper is trying to trick the system, attention should be paid to the use of paraphrased fragments.
+These factors effectively eliminate editorial efforts to verify the authenticity and originality of arguments and facts used in manuscripts submitted for publication.
+There is no processing or modification of Latin letters in Russian words to similar letters of the Russian alphabet for texts in Russian.
+The service allows replacing English letters with Russian letters.
+There is a limit on text length of 3000 characters.
+There is a limit on the number of checks per day.
+Search support for the own database is missing.
+The system does not perform searches using its own database.
+Due to operational characteristics, verification results may differ from one instance to another.
+Manual sampling is an alternative to automatic plagiarism detection.
+Manual searching cannot be as systematic as an automatic tool.
+Inconsistencies may arise in manual detection due to differing definitions of plagiarism within an organization.
 
```