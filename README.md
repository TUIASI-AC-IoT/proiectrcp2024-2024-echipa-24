# Proiect RC
**SNMP (Simple Networking Management Protocol) - Documentatie**

**Protocolul SNMP**

- Protocolul SNMP functioneaza la nivelul aplicatie al modelului TCP/IP si are ca scop monitorizarea si controlul dispozitivelor conectate la o retea. 

- In modul sau de operare de baza, SNMP este un protocol de Tip Cerere/Raspuns. Procesul care initiaza cererile si controleaza comunicarea se numeste Manager, iar procesul responsabil pentru furnizarea raspunsurilor se numeste Agent. Transmiterea pachetelor se realizeaza prin UDP(User Datagram Protocol).

- `MIB` (Management Information Base) este o componenta esentiala a SNMP. `MIB`-urile sunt baze de date in care se afla obiectele gestionate. Acestea sunt identificate prin `OID`, siruri de numere care definesc o structura erarhica(arborescenta).

![image](https://github.com/user-attachments/assets/185be542-d627-4285-b817-b8a97ee7b483)

  *Diagrama cu formatul generic pentru OID*


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

![image](https://github.com/user-attachments/assets/ad5f4b09-f895-412d-90a4-5623dab30061)

Atat resursele monitorizate cat si unitatile de masura si pragurile de alerte pentru fiecare resursa vor fi stocate in `MIB` si vor avea cate un `OID` astfel :
- `Temperatura CPU` : 1.3.6.1.2.1.1.1
- `Utilizare CPU` : 1.3.6.1.2.1.1.2
- `Temperatura GPU` : 1.3.6.1.2.1.2.1
- `Utilizare GPU` : 1.3.6.1.2.1.2.2
- `Memorie utilizata` : 1.3.6.1.2.1.3
- `Unitate de masura temperatura CPU` : 1.3.6.1.2.2.1.1
- `Unitate de masura temperatura GPU` : 1.3.6.1.2.2.1.2
- `Prag de alerta temperatura CPU` : 1.3.6.1.2.2.2.1.1
- `Prag de alerta utilizare CPU` : 1.3.6.1.2.2.2.1.2
- `Prag de alerta temperatura GPU` : 1.3.6.1.2.2.2.2.1
- `Prag de alerta utilizare GPU` : 1.3.6.1.2.2.2.2.2
- `Prag de alerta memorie utilizata` : 1.3.6.1.2.2.2.3

![OID2 drawio](https://github.com/user-attachments/assets/0befa480-c427-4027-92e6-bf8bb384f8a2)
  *Diagrama cu OID-urile custom folosite in proiect*

---
# Codificarea ASN.1 cu Regula BER (Basic Encoding Rules)

Codificarea **ASN.1** (Abstract Syntax Notation One) este un sistem standardizat pentru reprezentarea datelor intr-un format independent de limbajul de programare. Regula de codificare **BER** (Basic Encoding Rules) defineste cum sa codifici aceste date pentru a fi transmise sau stocate. Este folosita in diverse protocoale de retea, inclusiv **SNMP** (Simple Network Management Protocol).

## Principiul TLV (Tag-Length-Value)

Fiecare element ASN.1 este reprezentat de trei componente:

1. **T - Tag**: Identifica tipul datelor.
2. **L - Length**: Reprezinta lungimea datelor.
3. **V - Value**: Reprezinta datele efective.

---

## Detalii despre structura TLV

### 1. **T - Tag (Tipul datelor)**:
   - Este un octet (sau mai multi octeti) care identifica tipul si clasa datelor.
   - Tipurile sunt definite prin **numerice** standardizate:
     - **`0x02`**: INTEGER
     - **`0x04`**: OCTET STRING
     - **`0x06`**: OBJECT IDENTIFIER (OID)
     - **`0x30`**: SEQUENCE (pentru grupuri de elemente structurate)
     - **`0x05`**: NULL (pentru valori nule)

### 2. **L - Length (Lungimea datelor)**:
   - **Lungime scurta**: Daca lungimea este mai mica de 128, este codificata intr-un singur octet (`L`).
   - **Lungime lunga**: Daca lungimea este mai mare de 127, primul octet specifica numarul de octeti care urmeaza pentru lungime (`0x80 | numar_de_octeti`).

### 3. **V - Value (Valoarea efectiva a datelor)**:
   - Datele efective sunt codificate in functie de tipul de data specificat de tag. 

---

## Tipuri de Date Utilizate in SNMP

In cadrul SNMP, mai multe tipuri de date ASN.1 sunt utilizate pentru a reprezenta diferitele informatii si structuri din mesajele SNMP:

### 1. **INTEGER (`0x02`)**
   - **Codificare**: Valoarea este codificata in complement fata de doi.

### 2. **OCTET STRING (`0x04`)**
   - Reprezinta o secventa de octeti, folosita frecvent pentru a stoca siruri de caractere sau date brute.
   - Exemple: "public", "password", date binare.
   - **Codificare**: Sirul de octeti este direct codificat in secventa de valori.

### 3. **OBJECT IDENTIFIER (OID) (`0x06`)**
   - Reprezinta identificatori ierarhici, care sunt utilizati pentru a desemna obiecte dintr-un arbore de obiecte (de exemplu, `1.3.6.1.2`).
   - **Codificare**:
     - Primul octet este calculat ca `40 * primul_sub_id + al_doilea_sub_id`.
     - Urmatoarele octeti reprezinta sub-ID-urile, fiecare codificat in baza 128 (cu MSB = 1 pentru continuare).

### 4. **SEQUENCE (`0x30`)**
   - Reprezinta un grup de elemente structurate. In SNMP, se foloseste pentru a reprezenta grupuri de date, cum ar fi perechi OID-valoare.
   - **Codificare**: Este o colectie de elemente, fiecare codificata separat, urmata de o codificare a secventei.

### 5. **NULL (`0x05`)**
   - **Codificare**: Este codificata ca `0x05 0x00` (Tag-ul `0x05` si lungimea 0).

---
# Structura pachetelor SNMP

![image](https://github.com/user-attachments/assets/187ed143-000e-4015-9fc5-d3f425ed27b9)
               Structurea mesaj SNMP

![image](https://github.com/user-attachments/assets/9056b138-57fe-4346-8e36-b69a24b81cf4)
Structura PDU(Protocol Data Unit) GetRequest si SetRequest

![image](https://github.com/user-attachments/assets/54391e64-1409-4bf6-bbe5-78f457837cac)
Structura PDU(Protocol Data Unit) Trap

sursa imagini: **https://cdpstudio.com/manual/cdp/snmpio/about-snmp.html**

Porturile folosite:
    - **`161`**: Trimiterea si primirea pachetelor de tip `GetRequest`,`GetNextRequest`,`SetRequest`.
   
    - **`162`**: Trimiterea si primirea Trap-urilor.

Interfata realizata cu TKinter
![image](https://github.com/user-attachments/assets/11a04b2b-7f5b-4ef3-be27-c7197a43b10a)

    
- https://datatracker.ietf.org/doc/html/rfc1157
- https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol
- https://www.manageengine.com/network-monitoring/what-is-snmp.html
- http://www.tcpipguide.com/free/t_SNMPProtocolBasicRequestResponseInformationPollUsi.htm
- https://www.satel.com/wp-content/uploads/2017/08/13.-SATELLAR-and-SNMP-Get-SNMP-Set.pdf
- https://www.site24x7.com/network/what-is-snmp.html
- http://www.tcpipguide.com/free/t_SNMPProtocolMessagingandMessageFormats.htm
- https://www.oss.com/asn1/resources/asn1-made-simple/asn1-quick-reference/basic-encoding-rules.html
