# Document diff — Progear
*Sentence-level diff, original English → after the KPR merge. 221 lines added/changed.*

```diff
--- Progear (original English)
+++ Progear (after KPR merge)
@@ -26,7 +26,104 @@
 
+== Controls and Movement ==
+
+The player controls the ship using an 8-directional joystick and two buttons designated for Shot and Bomb.
+Depending on the board settings, a third button may function as an auto-fire shot.
+Rapidly tapping the shot button activates a high-speed movement mode focused on shooting known as Fighter Mode.
+Holding down the shot button activates an attack mode focused on the gunfighter that automatically targets enemies in all directions, called Gunner Mode.
+
+== Aircraft and Weapon Customization ==
+
+The two aircraft types differ in their firing characteristics, with one type having a wide spread shot capability and the other having a concentrated shot capability.
+It is possible to choose between three different types of cannons, each with a specific firing mechanism, where one type fires an explosive bomb, another fires a cannonball, and the third fires a homing missile.
+
+== Stage Structure and Visuals ==
+
+The player must navigate through mazes formed by enemy fire.
+Each level is very short and ends with a boss fight against large bosses.
+The stage background uses many dark colors, while the enemy bullets are blue, creating a strong contrast between the background and the bullets.
+Text information such as the score is displayed around the edges of the screen, moving out of the frame when the player's ship approaches and moving into the frame when the player's ship moves away.
+
+== Jeweling System Mechanics ==
+
+This system is called 'Jeweling' and is the most distinctive feature of this game.
+Jeweling is essential for completing the game, yet the instruction manual does not mention Jeweling.
+Jeweling can be triggered in Fighter Mode, where enemy bullets transform into rings when the system activates.
+The type of ring that appears depends on the number of enemy bullets involved in a single explosion.
+Amethyst rings appear first, followed by Ruby rings, then Emerald rings, and finally Diamond rings.
+These rings have high value, and Amethysts, Rubies, and Emeralds each exist in three sizes: small, medium, and large.
+The highest value ring obtained is recorded and appears in the corner of the screen.
+Only one type of gem with the same value as the recorded ring appears, and high-value gems yield higher scores than rings of the same value.
+A diamond ring is worth 100 points.
+
+Jewels are scattered on the screen, and a jewel counter located at the bottom of the screen increases based on the rings or gems obtained.
+In this game, shooting one shot adds 1/1000 to the jewel counter, and any fractional part below the ones place is truncated when adding to the jewel counter.
+A diamond gem is worth 1280 points, and the range of the effect is wider for higher-value gems.
+Jeweling occurs even when enemy bullets turn into gems due to the effect, and if gems created in the Gunner mode are attracted, their value is reset.
+If the Gunner mode ends after at least one gem appears, the ring value resets to the minimum.
+Determining the timing for collection is an important strategic element, and this mechanic is an important factor for achieving high scores.
+This mechanism creates a possibility for a comeback from a desperate situation and a possibility for achieving high scores.
+
+== Gunner Affection and Bonuses ==
+
+The Gunner's performance changes based on the 'Affection' parameter, which changes depending on the player's gameplay content.
+Bonuses can be applied to individual performance metrics and depend on the combination of the player's ship and the gunner.
+
+== Second Playthrough Conditions ==
+
+Clearing the 5th stage leads to a second playthrough if certain conditions are met, specifically if a specific condition is met upon clearing Stage 5.
+One of the conditions for entering the second playthrough is using two or fewer bombs, and the use of continues does not affect the bomb count condition.
+Another condition for entering the second playthrough is making one or fewer mistakes, and satisfying either the bomb condition or the mistake condition triggers the second playthrough.
+Building a Jewel pattern is almost essential to clear the game in two rounds, and the player must increase their lives to 9 during the first round before starting the second round.
+
+== Second Playthrough Changes ==
+
+The falling speed of the gems increases, the enemy composition changes, and the attack patterns change.
+These changes apply to both regular enemies and bosses.
+Defeating enemies causes them to fire back a large number of projectiles when hit.
+The dialogue spoken when defeated differs significantly between the first playthrough and the second playthrough, and the dialogue in the second playthrough is described as sorrowful.
+Volvox differs significantly between the first playthrough and the second playthrough, gaining one additional form and one additional attack pattern before being defeated in the second playthrough compared to the first.
+
+== Lives and Scoring Rules ==
+
+A mistake made during the stage causes a restart from the beginning of that stage.
+There is no life extension based on the score.
+The 1UP item can be obtained only once.
+
+== Bosses and Enemies ==
+
+Barossam-Pinch is a Stage 1 boss who commands the troops around the Gunflyer hangar and pilots a fish-shaped airship named Tobiuo.
+Gabriel Hammer is the Stage 2 boss who commands the harbor area and pilots a submarine named Hakugei.
+Jim Chuck Spanner is a Stage 3 boss who commands the forces near the imperial capital and pilots an armored vehicle named Korogis.
+Orsol=Nibber commands the mountainous region and pilots the airborne fortress Kraken.
+Leonardo Drill is the final boss whose mount is a spherical fortress named Volvox.
+The game uses a wide variety of irregular bullet patterns in enemy attacks.
+
+== Ending Presentation ==
+
+The ending animation is in manga format, and multiple patterns are prepared for the ending.
+
+This work is the only Cave product where Junya Inoue's manga can be read.
+
 The plot summary of Progear is explained through supplementary materials.
 Sometime in the past, people of the kingdom of Parts found a way to become immortal but only with elderly nobles.
+They obtained immortal bodies through cutting-edge technology.
 Among these elders who obtained immortality were Ballossum Pench, Gabriel Hammer, Jimchuck Spanner, Olsorro Slasher and Leonard Drill.
 They later became known as the Motoruin sages, eventually attempting to take over the Parts kingdom and began a new world order, collapsing the government and destroying villages of the country in the process.
+The kingdom of Parts developed its industry using a perpetual motion machine called 'Progia'.
+The Progia harnesses wind power.
 As their plans unfold, five children decided to battle the Motoruin using another new invention: the titular semi-automatic propelling engine.
+Dialogue becomes comical when the boss is defeated.
+The dialogue for the fourth stage boss is tragic instead of comical.
+Clearing all stages leads to the true ending regardless of affection level.
+The true ending is not available in the first playthrough unless the affection level is 5 or 6.
+In the True End with Ring, Ribbet accepts his marriage proposal.
+Ribbet was carrying the child of her superior officer at the time.
+This revelation causes inner conflict for Ring.
+Ribbet has positive feelings towards Ring.
+In the second playthrough, the immortal characters express regret for becoming immortal.
+The character's true face is revealed in the second playthrough.
+The Senate launched a great purge known as the 'Punishment of the Wise' in future generations.
+Eventually, only pilots of the Boy Air Force remained.
+The character names on the side of the Senate use disassembly tools.
+This change occurs due to the abolition of the monarchy.
 
@@ -38,14 +135,80 @@
 
+== Main Pilots and Gunners ==
+
+Reid is a young airman ace pilot voiced by Mitsuo Furusawa whose father was a noble airman that died in battle against the Senate.
+Chain is voiced by Aki Shibata [cite: 3] and dislikes relying on her family's influence.
+Chain and Ring have been partners for a long time, and their friendship stems from their fathers' connection.
+The character becomes Chain's partner, reaches the true ending with Chain, and marries Chain.
+Ring and Chain get married in the true ending.
+Bolt Boyer is voiced by Junya Inoue, his father is a politician, and he serves as the student council president at his academy.
+Nail is voiced by Midori Kato, is the last daughter of the Parts Kingdom royal family, and is skilled enough to overwhelm Bolt.
+She broke her right leg upon landing and was hospitalized as a result of the injury.
+
+Nail acts spoiled while using the wheelchair.
+
+== Supporting Characters ==
+
+Rebelle is a female soldier who has just joined the regular army and is voiced by Masayo Hirasaka.
+Revet serves as Nail's instructor and fights under the orders of a Colonel whose name does not appear in the story.
+The character speaks through a ventriloquist dummy during conversations.
+
+== Senate and Command ==
+
+Orsol=Nibber is the General Secretary of the Senate and the only female member of the Senate.
+Leonardo Drill is the Grand Marshal and the Supreme Commander who coordinates the members of the Senate.
+The character appears with a face resembling a lion, which is actually a mask.
+
+== Gambler Aircraft ==
+
+The Gambler is a twin-seat amphibious combat flying boat that uses a pusher engine layout.
+The vehicle has a slow movement speed and can attack over a wide area with a wide shot weapon.
+
+== Militant Aircraft ==
+
+The Militant is a twin-seat fighter aircraft with a conventional shape and a low-wing monoplane design.
+Its weapon is a concentrated shot with a narrow attack range, and its movement speed is fast.
+
+== Alpha and Beta Vehicles ==
+
+The Alpha model has a shape resembling an air-cooled engine with a cowling and attached winglets.
+Its weapon is an explosion missile that has high power and causes an explosion upon impact.
+The Beta model has a similar shape to the Alpha model, but its propellers are mounted facing backward.
+The Beta model's weapon is a cannonball that has a high fire rate and a wide attack range.
+
+== Gamma Vehicle ==
+
+The Gamma model resembles a helicopter, lacks a tail rotor, and lacks a canopy.
+Its weapon is a homing missile that ensures a certain hit.
+
+== Voice Cast ==
+
+Mitsuo Furusawa, Junya Inoue, Aki Sibata, Midori Katou, and Masayo Hirasaka provided voice acting.
+
+== Plot Details and Endings ==
+
+The name of the lizard is Kugui, a fact revealed in the True End involving Bolt.
+The True End for Ring does not mention the monarchy.
+
 Progear was a collaboration effort with Capcom by most of the same team that worked on previous projects at CAVE, serving as their first horizontally scrolling shooter game, in addition to being the six shoot 'em up title from the company and their eight video game overall.
+Cave is known for its vertically scrolling games.
 Kenichi Takano served as producer with director Junya Inoue.
 Tsuneki Ikeda served as chief programmer alongside Satoshi Kōyama and Takashi Ichimura.
+Tosiaki Tomizawa was an assistant.
 Akira Wakabayashi, Fusayuki Watariguchi, Hiroyuki Tanaka and Kengo Arai acted as designers.
+The illustrations for this work were provided by Junya Inoue.
 The soundtrack was composed by Yukinori Kikuchi, with Ryūichi Yabuki creating the sound effects.
-
+Development documents were included in the soundtrack released in 2014.
 The project originally went under the working title Propeller Wars early in development, before being renamed as Garden of Progear and was first envisioned as a vertical-scrolling shooter but Capcom remarked that the name was "too highbrow" and one of the higher-ups at CAVE told the team during their presentation pitch that the project should be a horizontal-scrolling shooter instead, with Ikeda revealing in a 2010 interview that the project was also intended to be their last release as the company was considering leaving the arcade market due to several factors at the time.
+This game was the world's first commercial horizontal scrolling bullet hell shooter.
+Human eyes are strong at vertical movement but weak at horizontal movement.
+This lack of acceptance was stated by Tsuneoki Ikeda of Cave.
 The team decided to make bullet dodging and enemy destruction its main focus, while adapting the company's shoot 'em up gameplay style in a horizontal format but the project would go through a problematic development cycle until it was released.
 Both Ikeda and Inoue stated that working with the CP System II platform, which marked the second time CAVE made use of an external arcade board, proved to be difficult as the hardware was underpowered compared to the previous board used for Guwange, with designers using a limited number of colors to remake drawings created in Photoshop.
-
 Inoue stated that the main characters were named after mechanical parts, while the reason having children as lead characters was both from an idea intended for a scrapped adventure game and due to his fascination of kids fighting against evil.
+The creators stated that they adopted a Steampunk style to reflect World War II.
+The creators stated that they adopted a Steampunk style to improve reception in Asia.
 Ikeda revealed that the team intended to feature four playable ships but the idea was scrapped due to time constrains, while Inoue also stated that the gender-based firepower pairing mechanic was a repurposed idea originally intended for a sequel to Batsugun.
+The game Death Smile was developed as a result of this reflection.
+Death Smile introduced a selectable difficulty system.
+Death Smile was designed to be easily playable by a wide range of people.
 
@@ -60,2 +223,40 @@
 
+== Initial arcade release ==
+
+The game was released in January 2001.
+The title of the game outside Japan is Progear.
+
+== Mobile phone ports ==
+
+This release is referred to as a port version.
+The service 'Gaisen Yokoyoko' was launched on April 28, 2004 and was available for mobile phones (iMode/Vodafone) [cite: 4,5,6].
+Users could play the titles 'Pro Gear no Arashi' and 'Pro Gear no Arashi DX' on a subscription basis [cite: 4,5,6].
+The service has now been discontinued [cite: 4,5,6].
+
+== Development challenges ==
+
+Porting to home platforms was not realized in Japan for a long time.
+In the past, developers at Cave Users Room stated that there was little demand and that sales were not expected.
+Cave Users Room developers stated that it was difficult to fully reproduce the main parts of the game because the game's main components, such as enemy bullet trajectories and dodging mechanics, are hard to replicate.
+This difficulty is due to the special aspect ratio of the CPS2 arcade board screen.
+
+== Capcom Home Arcade ==
+
+The Capcom Home Arcade, an arcade stick integrated game console, was announced by Capcom UK on April 16, 2019.
+The scheduled release date is October 25.
+The game's specifications are based on the operation of an emulator called FB Alpha and it uses overseas ROMs.
+
+== Capcom Arcade Stadium ==
+
+Capcom announced a release on December 11, 2020, for the downloadable software designed for the Nintendo Switch platform, which was scheduled to be released in February 2021.
+Capcom Arcade Stadium Pack 3: Arcade is taking it to the next level! was announced as one of the DLC packs for the product, and it was announced that 'Storm of Pro Gear' would be included.
+This is the first port of the arcade version in Japan.
+Capcom started selling the download software 'Capcom Arcade Stadium' for Nintendo Switch, with sales beginning on February 18, 2021.
+The announcement that PlayStation 4, Xbox One, and PC versions were planned for future release was made on the official website.
+The PlayStation 4, Xbox One, and PC versions were released on May 25 of that year.
+
+== Sequel ==
+
+The arcade game Progear's Storm was developed by Cave in 2001 and released by Capcom.
+
 In Japan, Game Machine listed Progear on their 1 June 2001 issue as being the fourth most-popular arcade game at the time.
@@ -66,6 +267,19 @@
 Carlos Leiva of Spanish website Vandal gave positive comments to the game's action, bosses, gameplay and original steampunk setting.
-David Jenkins of Metro praised its anime-style steampunk artwork design and accessibility, regarding it as "one of CAVE's best". oliveroidubocal of Jeuxvideo.com praised its visuals.
+David Jenkins of Metro praised its anime-style steampunk artwork design and accessibility, regarding it as "one of CAVE's best".
+oliveroidubocal of Jeuxvideo.com praised its visuals.
 However, Hardcore Gaming 101 remarked the music to be "the most lackluster thing" from the game.
 Nintendo Lifes Will Freeman regarded it as a standout shooter within the Capcom Arcade Stadium compilation due to its depth, visuals and replay value.
-
+Among shooting game enthusiasts, the difficulty of the second playthrough is said to be among the highest in shooting game history.
+A second playthrough clear without using a continue was achieved relatively early after the machine's operation began.
+This achievement was confirmed as early as August 2001 in the magazine Arcadia.
+The soundtrack includes original sound sources.
+The release consists of a single CD.
+The art collection contains setting materials, illustrations, rough sketches, and original artwork.
+The re-release included a CD containing digitized development materials and rough sketches or original drawings.
+The re-release was issued by the record label 'Super Record' (Sweep Record).
+The original work is titled 'Super Sweep'.
+Kikuchi Yukinori arranged the music.
+The official website for 'Storm of the Progear' was archived in 2011.
+'Storm of the Progear' includes a sound and art collection.
+The content introduces Capcom Arcade Stadium.
 Progear was featured in the music video for the song "Ikaruga" by the band Discordance Axis.
@@ -74 +288,4 @@
 Ring's Gambler plane with Chain's Alpha gunner appears as part of a Capcom-themed DLC for Dariusburst Chronicle Saviour.
+
+The record label Capcom Spirits belongs to Capcom.
+The soundtrack includes sound sources from CPS-2.
```