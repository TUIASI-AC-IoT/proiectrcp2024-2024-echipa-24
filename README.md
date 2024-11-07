# Proiect RC
**SNMP (Simple Networking Management Protocol) - Documentatie**

**Protocolul SNMP**

- Protocolul SNMP functioneaza la nivelul aplicatie al modelului TCP/IP si are ca scop monitorizarea si controlul dispozitivelor conectate la o retea. 

- In modul sau de operare de baza, SNMP este un protocol de Tip Cerere/Raspuns. Procesul care initiaza cererile si controleaza comunicarea se numeste Manager, iar procesul responsabil pentru furnizarea raspunsurilor se numeste Agent. Transmiterea pachetelor se realizeaza prin UDP(User Datagram Protocol).

- `MIB` (Management Information Base) este o componenta esentiala a modelului de management al retelei SNMP, definind formatul schimbului de informatii. `MIB`-urile sunt baze de date folosite de agenti in care se afla obiectele gestionate, numite `OID` (Object Identifiers). Acestea sunt identificate prin siruri de numere ierarhice care sunt asezate intr-o structura arborescenta.

![image](https://github.com/user-attachments/assets/185be542-d627-4285-b817-b8a97ee7b483)

**Despre agent**

Agentul este o aplicatie care ruleaza pe dispozitivul monitorizat, avand urmatoarele roluri:
- Colecteaza informatii despre mediul sau local.
- Stocheaza si recupereaza informatii de management conform definitiilor din MIB.
- Semnaleaza un eveniment catre manager.

**Despre manager**

Un manager este o aplicatie responsabil de comunicarea cu agentii SNMP implementati pe dispozitivele din retea. Acesta:
- Interogheaza agentii
- Primeste raspunsuri de la agenti
- Modifica variabilele agentilor
- Recunoaste evenimentele asincrone de la agenti

**Comenzi SNMP**
- `GetRequest` : Managerul trimite o cerere pentru a solicita valoarea unei variabile de la agent.
- `GetNextRequest` : Managerul trimite o cerere pentru a solicita urmatorul OID din MIB.
- `GetResponse` : Agentul trimite valoarea ceruta managerului.
- `SetRequest` : Managerul solicita modificarea unei variabile.
- `Trap` : Notificare asincrona de la agent catre manager.

![image](https://github.com/user-attachments/assets/f8ff02ca-e83e-4e27-ba7c-d553865cf4cd)

**Implementare**

Ne dorim realizarea a doua aplicatii: Manager si Agent, care pot comunica intre ele folosind protocolul SNMP. Se va folosi modulul socket, fara a interactiona in alt fel cu stiva de comunicatii.

Aplicatia de client va monitoriza periodic starea sistemului. In cazul primirii unei cerereri de tip `GetRequest` sau `GetNextRequest` va fi generat pachetul de raspuns in format `ASN.1` si il va trimite managerului, iar pentru `SetRequest` va modifica valoarea specificata si va trimite o confirmare. Daca se produc evenimente neasteptate(ex: cresterea brusca a temperaturii) va fi generat un mesaj de tip `Trap`. Se vor folosi 2 fire de executie, unul pentru monitorizarea starii sistemului, iar celalt pentru comunicarea efectiva.

![image](https://github.com/user-attachments/assets/86ea98ce-02ba-4ccf-b7cb-9da2d1bd98f0)

Aplicatia de manager are o interfata grafica care permite utilizatorului sa trimita cereri agentilor din retea, afisand totodata mesaj de tip `Trap`. Se va folosi un fir de executie pentru interfata grafica,unul pentru citirea `Trap`-urilor si se va crea un fir pentru fiecare schimb de mesaje cu un agent.
Actiuni posibile:
- GetRequest
- GetNextRequest
- SetRequest(Schimbare unitati de masura si Setare praguri alerte)

![image](https://github.com/user-attachments/assets/7018ed98-e0e8-429a-881e-800fa79f6386)


**Bibliografie**
- https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol
- https://www.manageengine.com/network-monitoring/what-is-snmp.html
- http://www.tcpipguide.com/free/t_SNMPProtocolBasicRequestResponseInformationPollUsi.htm
- https://www.satel.com/wp-content/uploads/2017/08/13.-SATELLAR-and-SNMP-Get-SNMP-Set.pdf
- https://www.site24x7.com/network/what-is-snmp.html
