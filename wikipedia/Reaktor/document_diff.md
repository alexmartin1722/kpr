# Document diff — Reaktor
*Sentence-level diff, original English → after the KPR merge. 189 lines added/changed.*

```diff
--- Reaktor (original English)
+++ Reaktor (after KPR merge)
@@ -7,3 +7,26 @@
 
+== Licensing and distribution ==
+
+Reaktor is proprietary software that operates under a proprietary license.
+It was created by Native Instruments, a German company based in Berlin.
+
+There was a version of the program called 'Reaktor Session' which was a simplified and limited version of the software.
+'Reaktor Session' was intended for users who did not want to create their own ensembles, only allowed users to use instruments created by others, and did not allow users to modify instruments.
+Reaktor Session was removed from the program by Native Instruments with the release of Reaktor version 5 [cite: 1].
+Ensembles created with Reaktor 5 cannot be used with Reaktor Session [cite: 1].
+The Reaktor Player was released in 2010 and serves as an equivalent to previous versions [cite: 1].
+Ensembles from version 5.5 can be played using the Reaktor Player [cite: 1].
+All versions support export in the form of DLLs which are not compatible with VST and can only be loaded in the Reaktor software.
+Version 2.3 supported DirectConnect plugins for Digidesign Pro Tools and MAS plugins for Mark of the Unicorn Digital Performer.
+Version 3.5 was released in 2002.
+Version 4 was released in 2003, improved VST performance, and added support for Audio Units.
+A limited-function version of REAKTOR called REAKTOR6PLAYER has been released and is available for free.
+Users can use these libraries on REAKTOR6PLAYER without purchasing REAKTOR.
+
+Stephan Schmitt began development in Berlin in 1994.
+The product was the first release by Native Instruments.
 In 1996, Native Instruments released Generator version 0.96 - a modular synthesizer for PC, requiring a proprietary audio card for low-latency operation.
+The proprietary sound card was developed in-house.
+GENERATOR Version 1.5 was released in 1998.
+GENERATOR Version 1.5 was redesigned to work with standard sound cards in a Windows environment.
 By 1998, Native Instruments redesigned the program to include a new hierarchy, and integrated third-party drivers for use with any standard Windows sound card.
@@ -25,9 +48,28 @@
 His contributions, along with those of Reaktor Core developer Martijn Zwartjes, were released within Reaktor 5 in April 2005.
+Reaktor 5 supports a 64-bit environment.
 Core Technology initially confused a lot of instrument designers because of its complexity, but is now steadily making its way into new instruments and ensembles.
-
-Reaktor 5.1, released on 22 December 2005, and presented as a Christmas present, features new Core Cell modules, and a new series of FX and ensembles.
+Reaktor 5.1, released on 22 December 2005, and presented as a Christmas present, features new Core Cell modules, a new series of FX and ensembles, and the Reaktor Core Technology.
+The released version is a free update.
+Version 5.1 added new factory presets.
+A sign bank module was added.
+A modal bank module was added.
 Also a number of bug fixes were also implemented.
-
 The release of Reaktor 5.5 was announced for 1 September 2010.
 It features a revised interface as well as other changes.
+Version 5.6 was released in 2011.
+The software supports 64-bit Windows environments.
+The software supports 64-bit MacOS environments.
+The image module supports PNG format.
+Version 5.7 was released in 2012.
+Version 5.7 included a wire debug mode.
+Version 5.8 added support for OSC.
+Version 5.8 added OSC-related modules.
+Version 5.8 improved MIDI processing.
+Version 5.8 improved sample management.
+Version 5.8 improved sampler-related modules.
+Version 5.9 was released in 2013.
+Integration with MACINE 2.0 host software was added.
+Support for Avid Pro Tools AAX plugins was added.
+The Primary library was redesigned.
+The Core Macro library was redesigned.
 
@@ -38,2 +80,43 @@
 
+== Release history and system requirements ==
+
+Version 6.1 was released in 2016, Version 6.2 was released in 2017, and Version 6.2.2 was released in 2018.
+Version 6.3.0 was released in 2019, and Version 6.4.2 was released in 2021.
+The file browser supports disks formatted with the APFS format on MacOS 10.13 and later versions.
+The software supports macOS Big Sur, and the 32-bit version is no longer provided starting from this version.
+
+== Audio processing and modulation tools ==
+
+A non-transposed nonlinear Siren filter, an 8-pole ladder filter with self-oscillation at Resonance-4, 6-pole and 8-pole Butterworth filters, and a Type II Butterworth filter with resonance were added.
+A phaser with a changeable notch count, a Barberpole/Through-zero Phaser and Flanger, and a Harmonic Phaser were added.
+An asymmetric Overdrive and an anti-aliased version of the asymmetric Overdrive were added.
+Bit/sample rate reduction and a Compressor were added.
+An LFO synchronized to tempo/transport position and an LFO toolkit were added.
+Zero-crossing detection event processing macros were added.
+Shelving filters were redesigned.
+
+== Blocks framework and GUI patching ==
+
+The Blocks framework underwent a complete overhaul and a new Rack mode was added.
+GUI-based patching was available at the time of the 6.3.0 release, allowing users to patch each block on the GUI without switching to the structure screen.
+This GUI-based patching was limited to Native Instruments official products and some third-party products.
+Patches can be saved within DAW sessions.
+The virtual modular ecosystem was opened to the NI community, enabling users to patch User Blocks within Racks and use blocks from the User Library.
+These blocks can be configured in Racks mode.
+Patching, playing, and saving are now easier to perform on the front of the panel.
+User Blocks can be accessed directly from the Library tab of the REAKTOR browser and searched using the search box within the Rack.
+The Extended view of Maschine allows applying panel patches.
+The Extended view of Komplete Kontrol allows applying panel patches.
+
+== Blocks content and free products ==
+
+Blocks Plumes was released simultaneously with the 6.3.0 release, includes 23 Blocks, includes over 50 presets, and is provided free of charge to Reaktor users.
+Komplete Start and Blocks Base were released as new free products.
+
+== Module updates and general improvements ==
+
+The sample map editor was improved, a full-screen feature in standalone mode was added, Ableton Link functionality was included, Logic added support for MIDI FX, and QuickBus copy and paste functionality was improved.
+The MASCHINE Sequencer module and the Niji Drums module were updated, and the modules support patching from Racks and from the front panel.
+A new Rack file format was added.
+
 From the end-user standpoint, Reaktor can behave as a sound creation/manipulation tool with a modular interface, provided there is enough CPU to manage its sample decryption processes.
@@ -59,2 +142,38 @@
 Each panel control in the ensemble is capable of MIDI automation in the host sequencer.
+
+== Core Architecture and Development Environment ==
+
+Reaktor is a graphical Integrated Development Environment used for creating and using software synthesizers, sequencers, samplers, and effect devices.
+A core component of Reaktor is an extensive collection of DSP modules used to generate and process audio and event data streams.
+From a technical perspective, there are three levels, with the original components located at the middle level.
+Reaktor is designed to facilitate the entry for beginners and allows engineers to design, build, and create their own instruments and sound effects.
+Reaktor is primarily used for sound generation, audio synthesis, and audio effects.
+
+== Modular Synthesis and Macro Creation ==
+
+This design freedom also enables the implementation of alternative interface concepts.
+Individual oscillators, envelope generators, filters, knobs, and display panels can be combined into macros.
+These macros serve as building blocks for instruments.
+Blocks represent partial instruments and are similar to Eurorack modules.
+The value ranges of the blocks are normalized, and the blocks do not distinguish between control and audio signals.
+These blocks enable the control of external hardware and allow people without technical training to have an easier entry point.
+Blocks Modules can simplify the handling of Reactor.
+REAKTOR Blocks are a set of modules provided for building synthesizers.
+Users can assemble various Blocks on REAKTOR to patch modular synthesizers.
+Each Block corresponds to a single module in a modular synthesizer.
+Several module sets are provided by default.
+The appearance resembles that of a modular synthesizer.
+
+== External Hardware Integration ==
+
+An audio interface capable of outputting DC signals can be used.
+Using such an interface allows for interoperability with modular synthesizers operating on a CV/GATE system.
+
+== System Compatibility and Plugin Formats ==
+
+Reaktor can run standalone and supports standalone operation.
+The software can be configured as a drum machine and as a sequencer.
+In Windows environments, the software supports ASIO and WASAPI.
+In MacOS environments, the software supports Core Audio.
+The software supports Audio Units plugins and AAX Native plugins.
 
@@ -69,2 +188,69 @@
 
+== Ensemble Types and Characteristics ==
+
+These instruments are grouped together into ensembles.
+Some ensembles are simple imitations of subtractive synthesizers, while others are complex generative ensembles.
+Generative ensembles use different algorithms and automatically produce constantly changing sounds.
+
+== Standalone Ensemble Products ==
+
+Native Instruments has started publishing individual ensembles as separate programs that can be used without owning Reaktor.
+The Analogic Filter Box is a product featuring Anima Banaan, Electrique Classic Vocoder, Cyan Echomania, EnFX Fast FX, Flatblaster Fusion Reflections, Grainstates FX, Longflow Resochord, Space Master 2, SpaceMaster Spring Tank, and Two Knees Compressor.
+GoBox, Krypt L3, Limelite, Massive 1.1, Newscool, Rhythmaker, and Sinebeats 2 are products.
+
+Splitter, Vectory, Random Step, and Shifter are products.
+The products are named BlueMatrix, WaveWeaver, and Spiral.
+
+== Matrix and Sequencer Ensembles ==
+
+The product includes the SQ16, SQ8, 8x8, SQ, and SQX models.
+The subject is named Skrewell.
+The list includes Equinoxe Deluxe, FM4, Gaugear, Green Matrix, Grobian, Junatik, Kaleidon, Lazerbass, Nanowave, Oki Computer 2, Photone, SoundSchool, Titan, and 2-Osc.
+
+The list includes Carbon, Analog, Steam Pipe 2, and SubHarmonic Sum.
+
+== Modular Components and Controls ==
+
+The Morph Filter is abbreviated as FLT, and the system includes a Shift Sequencer abbreviated as SEQ.
+The text mentions a ROUNDS Delay effect, a ROUNDS Reverb effect, and a ROUNDS LFO modulation.
+The device has a Scope input, a Clock input, and Gates and Triggers inputs.
+It features Macro Knobs and Macro Switches.
+The device has a MIDI Out port, a Note In port, a Pitch CV Out port, and a Trig In port.
+Controls on the device include a CV Mix, a Level Mono, a Level Stereo, and a Mix 4.
+
+== Additional Third-Party Libraries ==
+
+Additional libraries that run on REAKTOR have been released.
+Polyplex is a drum sampler and a musical instrument.
+The Finger is for performance, remixing, and effects.
+Molekular is a modular multi-effect system.
+The Mouth is a synthesizer and multi-effect unit.
+
+== Third-party support ==
+
+Third-party instruments were introduced specifically for REAKTOR and REAKTOR Player.
+Twisted Tools, Tim Exile, Heavyocity, Blinksonic, and Tonsturm products were made available as the first partner.
+
+== Educational resources ==
+
+Free Reaktor videos are provided by the London College of Music (LCM).
+
+== Comparison with SuperCollider ==
+
+SuperCollider is software that is not graphical, is programmable, and processes audio signals.
+
+== Specific ensemble features ==
+
+The device includes a VCA (Amplifier), an SVF (Filter), a Mix function, an XFade function, an ADSR Envelope module, an LFO (Low Frequency Oscillator) module, an Oscillator, a CV Processor, and a Sample & Hold processor.
+The device has 4 Modulation sources and 8 Steps in its sequencer.
+The subject is a Dual SKF system that includes FLT functionality and utilizes Multiwave technology.
+The system is an OSC (Optical Switching Component) with the specific model or version OSC 5.
+The component is a Quantizer and a Clock Divider.
+The subject is a product named DRIVER with the model or variant designation EFX.
+
+The system includes a Curve Sequencer, a Duality Oscillator (abbreviated as OSC), a Flip Generator, and a Morph Filter.
+
 Comparison of audio synthesis environments List of music software
+Max/MSP and Pure Data are main competitors of Reaktor.
+FlowStone, Max/MSP, OpenMusic, Pure Data, Quartz Composer, and SynthEdit are software tools.
+Pure Data is open-source.
```