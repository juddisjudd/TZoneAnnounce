# TZoneAnnounce
Small Application to display Current and Next Terror Zones in D2R.

Created with the purpose of using with OBS.

# How to use with OBS
- Download [latest release](https://github.com/juddisjudd/TZoneAnnounce/releases/download/1.0/TZoneAnnounce-1.0.zip).
- Extract .zip to a folder somewhere
- Run **TZoneAnnounce.exe** *(console window will come up showing current and next info)*
![](https://i.imgur.com/1KxPSv4.png)
- Create new "*Browser*" source in your OBS scene.
- Input url which will be your local ip followed by port 6060 (example: http://10.0.0.5:6060/)
![](https://i.imgur.com/vPmC9XK.png)

# Example Custom CSS options
```css
// Current & Next Zone
.zone-header {
    font-size: 36px;
}

// Zones Names
#currentZone, #nextZone {
    font-size: 24px;
	  color: #dfe6e9;
}
```

## CREDIT
[Mysterio @ D2EMU](https://www.d2emu.com/) - Thanks for the API
