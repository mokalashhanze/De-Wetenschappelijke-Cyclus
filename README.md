# De-Wetenschappelijke-Cyclus
# Introductie:
**Inleiding:**  
Goed slapen is heel belangrijk voor je lichaam en je hersenen. Als je slaapt, herstelt je lichaam van de dag. Je hartslag gaat tijdens het slapen omlaag omdat je lichaam helemaal tot rust komt. Als je een lage hartslag hebt in de nacht, betekent dit meestal dat je diep en goed slaapt. Je hart hoeft dan minder hard te werken. Daarom kijken we in dit onderzoek naar de hartslag, want die vertelt ons veel over hoe goed je slaapt.

**Onderzoek**  
In dit onderzoek bestuderen we de slaapkwaliteit door middel van een smartwatch die de hartslag tijdens het slapen meet. Dit onderzoek wordt uitgevoerd bij drie proefpersonen. We hopen met de resultaten mensen te kunnen helpen hun slaap te verbeteren. We weten dat ook andere factoren een rol spelen bij de hartslagmetingen, zoals het tijdstip van slapen, het type fysieke activiteit overdag, het tijdstip van de laatste maaltijd en telefoongebruik voor het slapengaan. Om deze factoren in kaart te brengen, vullen de proefpersonen dagelijks een korte vragenlijst in. Zo registreren we mogelijke storende variabelen die invloed kunnen hebben op de slaap en de hartslag.   

**Onderzoekvraag en hypothese:**    
Is de gemiddelde slaapkwaliteit, gemeten met de Fitbit-slaapscore, hoger bij een gemiddeld lagere hartslag tijdens de slaap? De verwachting is dat proefpersonen met een lagere gemiddelde hartslag tijdens de slaap beter slapen. Daarnaast wordt verwacht dat voldoende beweging overdag en het beperken van storende gewoonten, zoals schermgebruik voor het slapen, bijdragen aan een lagere hartslag en een betere slaapkwaliteit. Dit onderzoek is relevant omdat het inzichtelijk maakt hoe dagelijkse gewoonten invloed hebben op slaap en hartslag. Door deze verbanden beter te begrijpen, kunnen mensen bewustere keuzes maken voor een betere rust en optimaal herstel.   

**Gebruikte data:**   
Voor dit onderzoek gebruiken we de Fitbit-smartwatch om de hartslag te meten. De benodigde gegevens worden via een data-export uit de Fitbit-app gehaald. Dit bestand bevat alle relevante variabelen, waaronder de gemiddelde slaapkwaliteit en de gemiddelde hartslag tijdens de slaap. Via Google Forms registreren we de overige dagelijkse factoren met een vragenlijst. Met behulp van R-code analyseren we de data en genereren we een plot die de relatie tussen de slaapkwaliteit en de hartslag tijdens het slapen visualiseert.   

## Projectstructuur

Hieronder vind je een overzicht van de mappen en bestanden in deze repository:

* **analysis/**: De hoofdmap voor de analyses.
    * **data/**: Bevat de map met samengevoegde gegevens per persoon.
        * **combined_filetered/**: Bevat de gecombineerde databestanden (`combined_data_lucas.csv`, `combined_data_mohammed.csv` en `combined_data_robin.csv`).
    * **scripts/**: Bevat alle codebestanden voor de verwerking en analyse:
        * `csv_sort.py` / `csv_sort_combined.py`: Python-scripts voor het sorteren van data.
        * `analysis_eten_en_scherm_vs_slaapscore.Rmd`: R-Markdown script voor de analyse van maaltijden en schermtijd.
        * `LucasLogboek.Rmd`: Het persoonlijke logboek van Lucas.
        * `logboek_mohammed.Rmd`: Het persoonlijke logboek van Mohammed.
        * `logboek_robin.Rmd`: Het persoonlijke logboek van Robin.
* **docs/**: Documenten voor de onderbouwing van het onderzoek (zoals `Intro.md` en `Paper_Onderzoek.Rmd`).
* **protocols/**: Bevat het meetprotocol (`meetprotocol.md`) met de methodologie en afspraken.
* **raw_data/**: De basismappen met de originele Fitbit-exports per persoon (`takeout_lucas`, `takeout_mohammed` en `takeout_robin`).

### Proefpesonen: 

Dit onderzoek is uitgevoerd met een vaste groep van 3 volwassen proefpersonen: Lucas, Mohammed en Robin. Gedurende het experiment hebben zij allemaal dezelfde materialen gebruikt (de Fitbit Versa 4) en elke ochtend dezelfde vragenlijst ingevuld. Omdat de data van deze drie personen op exact dezelfde manier is verzameld, kunnen de individuele resultaten en gewoonten aan het einde van het onderzoek betrouwbaar met elkaar worden vergeleken.
