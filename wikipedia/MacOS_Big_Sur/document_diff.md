# Document diff — MacOS Big Sur
*Sentence-level diff, original English → after the KPR merge. 233 lines added/changed.*

```diff
--- MacOS_Big_Sur (original English)
+++ MacOS_Big_Sur (after KPR merge)
@@ -16,3 +16,9 @@
 Providing some indication as to how the pre-release operating system may have been viewed internally at Apple during its development cycle, documentation accompanying the initial beta release of macOS Big Sur referred to its version as "10.16", and when upgrading from prior versions of macOS using the Software Update mechanism to early beta releases, the version referred to was "10.16".
-An exception to this was the Developer Transition Kit, which always reported the system version as "11.0". macOS Big Sur started reporting the system version as "11.0" on all Macs as of the third beta release.
+The first beta version of macOS Big Sur was released shortly after the Worldwide Developers Conference (WWDC).
+The first public beta was released in August 2020.
+An exception to this was the Developer Transition Kit, which was released in 2020, manufactured by Apple for developers to test and develop, and always reported the system version as "11.0".
+The Developer Transition Kit has 16 GB of RAM and a 512 GB SSD hard drive storage.
+The Developer Transition Kit includes Xcode 12 for developers to use, and the chip used in the Developer Transition Kit is the same model as the one in the new iPad Pro.
+Universal 2 is used when opening a project in Xcode 12 Beta or later.
+macOS Big Sur started reporting the system version as "11.0" on all Macs as of the third beta release.
 
@@ -20,6 +26,22 @@
 
+== Naming and versioning ==
+
+The name change was intended to align Apple's software naming conventions, and the name is derived from Big Sur State Park.
+The version number increase was a symbolic gesture that accompanied Apple's transition from Macs using third-party processors to those using Apple's own developed processors, and the new version was not released as 10.16 as previously predicted.
+Since then, macOS versions have been numbered sequentially, with macOS 11 following macOS 10.
+
+== Announcement ==
+
+Craig Federighi, the Senior Vice President of Software Engineering at Apple, made a statement regarding the unveiling of Big Sur.
+
 Unlike macOS Catalina, which supported every standard configuration Mac that Mojave supported, Big Sur drops support for various Macs released in 2012 and early 2013.
-Big Sur runs on the following Macs:
-
-iMac (Mid 2014 or later) iMac Pro (2017) MacBook (Early 2015 or later) MacBook Air (Mid 2013 or later) MacBook Pro (Late 2013 or later) Mac Mini (Late 2014 or later) Mac Pro (Late 2013 or later) Developer Transition Kit (only up to Big Sur 11.3 beta 2) By using patch tools, macOS Big Sur can be installed on earlier computers that are officially unsupported, such as the 2012 iMac and the 2012 MacBook Pro.
+Big Sur is the second version of macOS to support 64-bit applications exclusively, following the release of macOS Catalina.
+Apple modified the list of supported devices, and this support is different from previous macOS versions such as Catalina.
+Big Sur runs on the following Macs: iMac (Mid 2014 or later), iMac Pro (2017), MacBook (Early 2015 or later), MacBook Air (Mid 2013 or later), MacBook Pro (Late 2013 or later), Mac Mini (Late 2014 or later), Mac Pro (Late 2013 or later), and the Developer Transition Kit (only up to Big Sur 11.3 beta 2).
+Support for 2013 iMac models was dropped.
+The iMac Pro is compatible with software or updates released from mid-2014 onwards.
+The Mac Pro is compatible with software or updates released from mid-2014 onwards.
+The Developer Transition Kit model from 2020 is eligible.
+macOS Big Sur requires at least 4 GB of RAM.
+By using patch tools, macOS Big Sur can be installed on earlier computers that are officially unsupported, such as the 2012 iMac and the 2012 MacBook Pro.
 Using these methods, it is possible to install macOS Big Sur on computers as old as a 2008 MacBook Pro and iMac and 2009 Mac Mini.
@@ -35,4 +57,48 @@
 
+== Scope and design philosophy ==
+
+Big Sur is considered the most extensive technical and visual update since Yosemite, and its underlying techniques were aligned with mobile operating systems, specifically iOS 14 and iPadOS 14. macOS is moving towards iOS, and the new style lies between skeuomorphism and flat design, a style that was introduced with iOS 13.
+Approximately 13 years have passed since version 10.5 Leopard, and the user interface in macOS Big Sur has been redesigned from scratch.
+
+== Visual style and color ==
+
+Larger rounded corners, increased spacing, a new color palette, and translucent backgrounds are among the most noticeable visual changes.
+The window edges now have a transparent effect and the window corners are rounded.
+Applications can now have an accent color on a per-application basis.
+Dynamic backgrounds were introduced.
+
+== Iconography and symbols ==
+
+The icons feature larger rounded corners, and the corners of icons and windows are rounded.
+SF Symbols have been updated and were previously used on iOS.
+
+== Window and toolbar changes ==
+
+The redesign included windows, and window title bars and icon bars were combined [cite: 30].
+The toolbar was redesigned, window maximization was expanded, and all pre-installed apps have a new sidebar [cite: 31,32,10,11,12,13].
+
+== Menu bar and Dock updates ==
+
+The menu bar is positioned higher up, is transparent, has become more transparent, and has rounded corners.
+The Dock is no longer anchored to the edge of the screen, now floats, has rounded corners, and has become more transparent.
+
+== Cross-platform integration ==
+
+The updated applications have an interface similar to iPadOS.
+
+== Startup sound ==
+
+The startup sound is slightly different from the previous one and has a lower pitch.
+
+== Weather ==
+
+The notification is sent when authorities issue a weather alert.
+It is possible to view a graph that shows rainfall intensity displayed on an hourly basis.
+
 An interface with quick toggles for Wi-Fi, Bluetooth, screen brightness and system volume has been added to the menu bar.
 This interface is functionally and visually similar to the Control Center on iOS and iPadOS.
+The control center is presented as a widget and is accessible via an icon in the menu bar.
+The Control Center allows access to main system settings.
+Control Center is a feature that allows quick changes to settings like Wi-Fi, Bluetooth, and AirDrop.
+It takes only one click to call up the Control Center, a method that differs from the iOS version.
 
@@ -40,2 +106,14 @@
 Notification Center also features a new widget system similar to that in iOS 14, displaying more information with more customization than previously available.
+The Notification Center aggregates notifications from applications and displays these aggregated notifications.
+Notification grouping was added to the Notification Center.
+The size and placement of the widgets became more flexible.
+Widgets for the Notification Center can be searched in the Mac App Store.
+The widgets support third-party sharing and enable family sharing of app subscriptions.
+Users can add Siri results to the Notification Center.
+
+macOS Big Sur ended the use of kernel extensions, which were used by applications to modify low-level system settings, and these programs now run separately from the operating system.
+DriverKit is a replacement solution proposed by Apple since macOS Catalina that allows programs to move from kernel space to user space.
+The system supports WebP images at the system level.
+The operating system received UNIX 03 certification from The Open Group, which applies to both the Apple Silicon version and the Intel version.
+macOS Big Sur abandoned kernel extensions, a change that increases system protection against vulnerabilities during software installation, improves cybersecurity, and makes the system lighter.
 
@@ -47,3 +125,42 @@
 
+== Apple Silicon architecture and transition ==
+
+macOS Big Sur marks the beginning of a transition for Apple's Macintosh personal computer line and was designed for future Macintosh computers.
+The new processors are called "Apple Silicon" and are intended for future Mac devices.
+These new ARM-based SoCs are similar to those found in iPhones and iPads [62,63], and the 64-bit ARM architecture (ARM64) is already used in iPhones and iPads.
+Apple's M1 chip is based on the same ARM architecture as mobile chips.
+The processor will replace currently used Intel processors.
+The goal of supporting ARM architecture is to improve performance and maximize energy efficiency.
+Apple stated that the transition could take up to 2 years [61,66], and Apple committed to completing the transition to Apple Silicon within two years.
+The system will switch to a complete ARM architecture in two years.
+
+== Developer Transition Kit and A12Z Bionic ==
+
+The Developer Transition Kit is available.
+The A12Z Bionic chip is the same chip used in the 2020 iPad Pro.
+Apple claims that most applications will run without issues.
+The A12Z Bionic chip was also used in the 2020 iPad Pro.
+
+== M1 chip and initial devices ==
+
+macOS Big Sur is the first macOS optimized for Macs with Apple's own ARM64-based M1 chip.
+These Macs are equipped with the M1 chip and must be running macOS Big Sur.
+
+== Rosetta 2 translation technology ==
+
+Rosetta 2 is an updated version of an emulator that performs x86 emulation.
+It performs static and dynamic binary recompilation.
+Rosetta translates code from x86 to ARM during application installation and during execution for dynamic libraries.
+
+== Universal 2 binary format ==
+
+Universal 2 was included in Xcode 12.
+
+== Application compatibility and performance ==
+
+Apple claims that most applications will run smoothly.
+
 On Macs based on Apple silicon, macOS Big Sur can run iOS and iPadOS applications natively and without any modifications needed from developers, aside from allowing the app to be available on the Mac App Store.
+This capability was made possible due to Apple Silicon (ARM CPU) and future Macs.
+Apple expects the update to simplify software development for multiple Apple platforms.
 The first Macs with this capability are those that use the Apple M1 SoC (system on a chip).
@@ -51,2 +168,4 @@
 Time Machine, the backup mechanism introduced back in Mac OS X 10.5 Leopard, has been overhauled to utilize the APFS file system (introduced in MacOS High Sierra) instead of the outdated HFS+.
+Previous versions of macOS could only back up to units formatted with HFS+.
+Apple's macOS 11 beta release notes document support for APFS-formatted backup volumes.
 Specifically, the new version of Time Machine makes use of APFS's snapshot technology.
@@ -55,3 +174,2 @@
 A more modest yet nevertheless significant advantage was noted as well for backups to network-attached disks.
-
 New local (i.e.
@@ -59,10 +177,11 @@
 There is no option to convert existing, HFS+-based backups to APFS; instead, users who want to benefit from the advantages of the new, APFS-based implementation of Time Machine need to start with a fresh volume.
-
 In the new version of Time Machine, encryption appears to be required (instead of merely optional) for local disks, but it remains elective for networked volumes.
-
 It is no longer possible to restore the whole system using a Time Machine backup, as the signed system volume is not backed up.
-Non -core applications and user data can be restored in full using Migration Assistant, preceded by a system reinstall if necessary.
+Non-core applications and user data can be restored in full using Migration Assistant, preceded by a system reinstall if necessary.
 
 Spotlight, the file system indexing-and-search mechanism introduced in Mac OS X 10.4 Tiger, is faster and the interface has been refined.
+Spotlight functionality was integrated into Finder.
 Spotlight is now the default search mechanism in Safari, Pages, and Keynote.
+Users can highlight dictionary results directly in Spotlight.
+Users can open the Dictionary app directly from Spotlight using the search term entered.
 
@@ -70,3 +189,6 @@
 Apple indicates this is a security measure to prevent malicious tampering.
+Apple expects the update to secure the platform.
 This includes adding an SHA-256 hash for every file on the system volume, preventing changes from third-party entities and the end user.
+There is a feature to check or block processes at the system level.
+Extension privacy management was added as a security feature.
 
@@ -74,2 +196,3 @@
 Because system files are cryptographically signed, the update software can rely on them being in precise locations, thus permitting them to be effectively updated in place.
+Updates were made to load faster.
 
@@ -79,3 +202,11 @@
 
-Bilingual dictionaries in French–German, Indonesian–English, Japanese–Simplified Chinese and Polish–English Better predictive input for Chinese and Japanese users New fonts for Indian users The "Now Playing" widget has been moved from the Notification Center to the Menu Bar Podcasts "Listen Now" feature FaceTime sign language prominence Network Utility has been removed The macOS startup sound is now enabled by default (it had been disabled by default on some machines released in 2016), and an option in System Preferences was added to enable or disable this functionality.
+Bilingual dictionaries in French–German, Indonesian–English, Japanese–Simplified Chinese and Polish–English Additional bilingual dictionaries were added to the Lexikon software Better predictive input for Chinese and Japanese users New fonts for Indian users The "Now Playing" widget has been moved from the Notification Center to the Menu Bar Podcasts "Listen Now" feature FaceTime sign language prominence Network Utility has been removed The macOS startup sound is now enabled by default (it had been disabled by default on some machines released in 2016), and an option in System Preferences was added to enable or disable this functionality.
+AirPods can now switch automatically between devices This automatic switching requires iOS 14 and iPadOS 14 If a call arrives from an iPhone while using a Mac, the AirPods will automatically switch to the iPhone The optimized charging feature has been implemented Optimized charging reduces battery wear Optimized charging increases battery longevity Usage controls were added
+
+Significant improvements to FaceTime sign language support have been made.
+
+== Music ==
+
+Users can discover new artists and new mixes on the 'Listen Now' panel.
+Search has been significantly improved, and suggestions are provided based on user preferences.
 
@@ -95,7 +226,44 @@
 
+== Interface redesign ==
+
+The Safari browser was significantly redesigned with a completely renewed interface.
+Individual tabs now display a favicon, and the new start page features improved tab design.
+Safari 14 includes and features an improved tab design [cite: 71,72][cite: 80,81].
+Users can choose whether to display the favorites panel, Siri suggestions, the most visited sites, the reading list, iCloud information, or the privacy report [cite: 24].
+
+== Performance and standards ==
+
+Apple claims that Safari's performance is significantly better than Google Chrome and Mozilla Firefox.
+Apple also claims that Safari is faster than Google Chrome and is 50% faster than Google Chrome.
+Safari supports HTTP/3, which is an experimental feature available since this operating system version.
+
+== Privacy and tracking ==
+
+The browser blocks trackers from websites that aim to track user searches to create a profile of user habits.
+Blocked trackers are displayed on the start page and shown next to the search bar.
+
+== Extensions and compatibility ==
+
+Google Chrome extensions can now be converted into Safari extensions, a process facilitated by tools provided by Apple.
+There is a preview page for importing passwords from Chrome.
+Extensions can now be downloaded from the App Store.
+
+== Translation features ==
+
+The translation function is currently in beta version.
+
 The Messages app was rewritten to be based upon Apple's Catalyst technology to enable it to have feature parity with its iOS counterpart.
+This ease of use is achieved through Catalyst.
 The new version of the app included a refined design as well as the ability to pin up to nine conversations that can sync across iOS, iPadOS and macOS.
 Users were also now allowed to search for messages and share their names and photos.
+Users can search for links directly in the chat.
+Users can search for photos directly in the chat.
+Users can search for videos directly in the chat.
+Users can search for documents directly in the chat.
+Users can search for trending images.
+Users can search for trending GIFs.
+Users can share these images and GIFs.
+Users can share GIFs in messages.
+Users can share videos in messages.
 Photo thumbnails could now also be used for group chats on the app.
-
 In addition, users could mention contacts by putting the @ symbol in front of their name.
@@ -103,11 +271,21 @@
 Memojis, 3d avatars were also made available on Messages.
+The Messages app includes stickers.
+The Messages app has a Memoji editor.
+The app offers stickers and an Memoji editor.
+The Messages app includes Memoji stickers and an editor.
 On Messages, users could now select photos based on parameters.
-
+Conversations can be categorized.
 In India, text message effects were added when users sent certain texts (e.g., texting "Happy Holi" will result in users seeing effects).
+Examples of message effects include confetti.
+Examples of message effects include balloons.
+Examples of message effects include laser beams.
 
 Refinements and new features of the Mac App Store include: A new "nutrition label" section dedicated to the data and information an app collects, also featured in the iOS App Store A new extensions category for Safari Third party Notification Center widgets, similar to those also added in iOS and iPadOS 14.
-The ability to share in-app purchases and subscriptions on the Mac via iCloud Family Sharing
+The ability to share in-app purchases and subscriptions on the Mac via iCloud Family Sharing allows administrators to share in-app purchases with other family members, and all family members will have access to the shared content.
 
 Collapsible pinned section Quick text style and formatting options Scanning enhancements
-
+The font can be easily changed using the Aa button.
+The list can now be expanded, and the most relevant results will appear at the top.
+
+The Photos application was updated.
 New editing capabilities Improved Retouch tool New zooming feature in views
@@ -115,2 +293,3 @@
 "Look Around" interactive street-level 360° panoramas, first implemented in the iOS 13 version of Maps, have been incorporated into the macOS version of Maps.
+It is now possible to see the interior of some buildings, including airports and shopping centers.
 Availability of directions for cyclists.
@@ -118,6 +297,23 @@
 Guides for exploring new places.
-
-A file structure has been implemented to allow organization of recordings in folders Recordings can be marked as Favorites for easier subsequent access Smart Folders automatically group Apple Watch recordings, recently deleted recordings, and Favorites Audio can be enhanced to reduce background noise and room reverb
+Limited traffic zones (ZTL) can be displayed, with the respective costs for these zones shown.
+The application will show routes to avoid the restricted traffic zones and will suggest the fastest route.
+
+A file structure has been implemented to allow organization of recordings in folders.
+Recordings can be marked as Favorites for easier subsequent access.
+It is now possible to save recordings, which are stored in a section called 'favorites'.
+Smart Folders automatically group Apple Watch recordings, recently deleted recordings, and Favorites.
+Audio can be enhanced to reduce background noise and room reverb.
+The feature is now implemented directly in the app.
+Voice Memos is available.
 
 About This Mac Activity Monitor AirPort Utility Archive Utility Audio MIDI Setup Automator Bluetooth File Exchange Books Boot Camp Assistant Calculator Calendar Chess ColorSync Utility Console Contacts Dictionary Digital Color Meter Directory Utility Disk Utility DVD Player Expansion Slot Utility FaceTime Feedback Assistant Find My Finder Folder Actions Setup Font Book Grapher Home Image Capture iOS App Installer Keychain Access Mail Launchpad Migration Assistant Mission Control Music Network Utility News (only available for Australia, Canada, United Kingdom, and United States) Photo Booth Podcasts Preview QuickTime Player Reminders Screenshot (succeeded Grab since macOS 10.14 Mojave) Script Editor Siri Stickies Stocks Storage Management System Information Terminal TextEdit Ticket Viewer Time Machine TV VoiceOver Utility Wireless Diagnostics
+The News application was transferred from iOS to macOS.
+The Finder application was also updated.
+Netflix and Disney+ 4K are supported on Mac using Apple's T2 chip.
+GarageBand may not be pre-installed.
+iMovie may not be pre-installed.
+Keynote may not be pre-installed.
+The Numbers app may not be pre-installed.
+The Pages app may not be pre-installed.
+XQuartz may not be pre-installed.
 
@@ -128,8 +324,8 @@
 Many of these were 2013 and 2014 MacBook Pros, though problems were also observed on a 2019 MacBook Pro and an iMac from the same year.
+The installation problems occurred in the early hours after the release.
 The initial rollout also disrupted Apple's app notarization process, causing slowdowns even on devices not running Big Sur.
-Users also reported that the update was slow or even might fail to install. macOS Catalina and Big Sur apps were taking a long time to load because of Gatekeeper issues.
-
+Users also reported that the update was slow or even might fail to install.
+macOS Catalina and Big Sur apps were taking a long time to load because of Gatekeeper issues.
 The issues with the COVID-19 pandemic meant it was hard for users to visit an Apple Store to get their machines fixed.
 Shortly afterwards, Apple released a series of steps explaining how these Macs could be recovered.
-
 Certain Apple applications running on early versions of Big Sur were reported to bypass firewalls, raising privacy and security concerns.
@@ -139,5 +335,11 @@
 Apple responded that the process is part of efforts to protect users from malware embedded in applications downloaded outside of the Mac App Store.
-
+Security measures of the operating system are considered a blatant intrusion into user privacy by critics.
+Criticism regarding the operating system's security measures is based on a blog post by Berlin hacker Jeffrey Paul.
+The criticism specifically targets the fact that the operating system communicates with Apple servers every time a program is opened.
+This communication occurs to validate the opening process.
+The user would disclose information about their location.
+The user would disclose other private information, such as Internet service provider or IP address.
+This information could be spied on and analyzed by Apple.
+This information could be spied on and analyzed by third parties, such as intelligence agencies.
 Some users have reported problems connecting external displays to Macs running Big Sur 11.1 and 11.2.
-
 When upgrading Macs from 10.13, 10.14 and 10.15 to Big Sur the upgrade process could become stuck for seemingly unclear reasons.
@@ -153,2 +355,13 @@
 Version 11.0 was preinstalled on Apple silicon Macs, and Apple advised those with that version to be updated to 11.0.1.
+It was scheduled for release in the fall of 2020.
+macOS Big Sur is distributed for free.
+In this release, point releases increase the second component of the version number.
+In previous releases, point releases increased the third component of the version number.
+In previous releases, major releases increased the second component of the version number.
+Now, macOS uses major version numbers for system updates, similar to iOS.
+This is the first version of macOS distributed as IPSW recovery files.
+These files are for Mac computers based on Apple silicon.
+The latest version of the operating system is 11.7.10.
+Version 11.7.10 was released on September 11, 2023.
+Apple discontinued support for macOS 11 Big Sur on November 30, 2023.
 
```