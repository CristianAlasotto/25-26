# Indice dettagliato — Appunti completi di Complementi di Reti

## 1. Fondamenti del livello di rete *(pag. 1)*

### 1.1 Obiettivi del livello di rete
- Interconnessione tra reti locali eterogenee
- Introduzione di un livello software comune
- Ruolo dei router
- Sistema di indirizzamento IP

### 1.2 Forwarding e Routing
- Forwarding o inoltro
  - Processo locale al singolo router
  - Analisi dell’intestazione del pacchetto IP
  - Consultazione della forwarding table
  - Scelta dell’interfaccia di uscita
- Routing o instradamento
  - Processo distribuito
  - Calcolo dei percorsi migliori
  - Popolamento automatico delle tabelle di inoltro

### 1.3 Algoritmi e metriche di routing
- Metriche statiche
  - Numero di nodi attraversati
  - Costi amministrativi
  - Ritardo statico
- Metriche dinamiche
  - Carico dei collegamenti
  - Ritardo corrente
  - Stato della rete in tempo reale

### 1.4 Famiglie di algoritmi di routing
- Distance Vector
  - Conoscenza locale della rete
  - Scambio di informazioni tra router vicini
  - Algoritmo di Bellman-Ford
  - Protocolli RIP e IGRP
- Link State
  - Costruzione della topologia completa
  - Conoscenza globale dello stato dei collegamenti
  - Algoritmo di Dijkstra
  - Protocollo OSPF
- Path Vector
  - Instradamento tra domini amministrativi
  - Sequenza degli Autonomous System attraversati
  - Protocollo BGP
- Flooding
  - Duplicazione dei pacchetti sui collegamenti
  - Robustezza
  - Elevato costo in termini di traffico

### 1.5 Differenze tra host e router
- Stack di rete degli host
- Tabelle di routing locali
- Interfacce di rete fisiche
- Interfaccia virtuale di loopback
- Router e gateway
- Gestione dei pacchetti non destinati direttamente al router
- Funzione di forwarding


## 2. Suite FRRouting — FRR *(pag. 2)*

### 2.1 Introduzione a FRRouting
- Evoluzione dei progetti Zebra e Quagga
- Utilizzo di Linux come router avanzato
- Protocolli supportati
  - RIP
  - OSPF
  - IS-IS
  - BGP

### 2.2 Architettura modulare di FRR
- Daemon specifici per protocollo
  - `ripd`
  - `ospfd`
  - `bgpd`
- Daemon centrale `zebra`
- Comunicazione tra daemon
- Installazione delle rotte nel kernel Linux

### 2.3 Configurazione tramite VTYSH
- Shell unificata `vtysh`
- File `/etc/frr/daemons`
- Selezione dei daemon da avviare

### 2.4 Livelli di privilegio di VTYSH
- Utente non privilegiato
- Modalità privilegiata
- Modalità configurazione

### 2.5 Configurazione operazionale di FRR
- Configurazione operazionale e non dichiarativa
- Rimozione dei comandi tramite prefisso `no`

### 2.6 Principali comandi VTYSH
- `?`
- `configure`
- `enable`
- `exit`
- `quit`
- `no`
- `ping`
- `show`
- `terminal`
- `write`


## 3. Misurazione delle prestazioni con iperf3 *(pagg. 2-4)*

### 3.1 Introduzione a iperf3
- Generazione di traffico sintetico
- Analisi dei limiti fisici e logici della rete
- Modello client-server

### 3.2 Architettura client-server
- Server iperf3
  - Porta TCP 5201
  - Comando `iperf3 -s`
  - Esecuzione in background
  - Opzione `-D`
- Client iperf3
  - Connessione al server
  - Generazione del traffico
  - Calcolo delle statistiche
  - Comando `iperf3 -c <IP_SERVER>`

### 3.3 Misurazione delle prestazioni TCP
- Affidabilità del protocollo TCP
- Limiti introdotti dai meccanismi di controllo

#### 3.3.1 Flussi TCP paralleli
- Limiti di un singolo flusso
- Congestion Window
- Apertura di connessioni simultanee
- Opzione `-P`
- Esempio: `iperf3 -P 4`

#### 3.3.2 TCP Window Size
- Dimensione dei buffer TCP
- Relazione con la latenza

#### 3.3.3 Bandwidth-Delay Product — BDP
- Quantità di dati contemporaneamente in transito
- Formula:

  `BDP = Bandwidth × RTT`

- Configurazione della finestra tramite opzione `-w`

#### 3.3.4 Algoritmi di controllo della congestione
- TCP Reno
- TCP CUBIC
- TCP BBR

### 3.4 Misurazione UDP e Quality of Service
- Caratteristiche del protocollo UDP
- Applicazioni real-time
  - VoIP
  - Streaming
  - Gaming
- Modalità UDP `-u`
- Configurazione della banda tramite `-b`

### 3.5 Parametri delle applicazioni real-time
- Packet Loss
- Jitter
- Conseguenze del jitter elevato
- Ritardi e riproduzione audio

### 3.6 Integrazione tra iperf3 e Linux Traffic Control
- Utilizzo con il comando `tc`
- Simulazione di reti degradate
- Validazione delle policy di rete

#### 3.6.1 TBF — Token Bucket Filter
- Limitazione della banda in uscita
- Verifica del limite tramite iperf3

#### 3.6.2 NetEm — Network Emulator
- Simulazione di:
  - Delay
  - Jitter
  - Packet loss
  - Condizioni di rete degradate

#### 3.6.3 HTB — Hierarchical Token Bucket
- Creazione di classi di traffico
- Corsie preferenziali
- Gestione gerarchica della banda

### 3.7 Automazione e scripting
- Output JSON tramite opzione `-J`
- Integrazione con script Python
- Monitoraggio automatico
- Estrazione delle metriche
  - Dati inviati
  - Dati ricevuti
  - Jitter UDP
- Generazione automatica di grafici


## 4. Protocollo RIP e algoritmo Distance Vector *(pagg. 4-5)*

### 4.1 Principi del protocollo RIP
- Algoritmo Distance Vector
- Algoritmo di Bellman-Ford
- Scambio delle informazioni tra router vicini
- Aggiornamento delle tabelle di routing

### 4.2 Processo di convergenza
- Aggiornamenti iterativi
- Calcolo dei percorsi minimi
- Condizione di convergenza
- Stabilizzazione delle tabelle

### 4.3 Problema del Count-to-Infinity
- Guasto di un collegamento
- Informazioni obsolete
- Creazione di routing loop
- Incremento progressivo della metrica
- Tempi di riconvergenza elevati

### 4.4 Poisoned Reverse
- Prevenzione dei routing loop
- Annuncio di una distanza infinita
- Impedimento del riutilizzo del percorso
- Accelerazione della convergenza

### 4.5 Implementazione di RIPv2 in Kathará e FRRouting
- Avvio manuale di FRR
  - `systemctl start frr`
- Accesso alla shell
  - `vtysh`
- Abilitazione del protocollo RIP
- Annuncio delle reti locali
  - Comando `network`
- Comunicazione multicast RIPv2
  - Indirizzo `224.0.0.9`
- Configurazione delle stub network
- Rotta statica predefinita
  - `ip route add default via ...`
- Propagazione della default route
  - `route 0.0.0.0/0`
- Comando `redistribute connected`
- Propagazione delle reti direttamente connesse


## 5. Introduzione a IPv6 *(pagg. 5-6)*

### 5.1 Passaggio da IPv4 a IPv6
- Limite dello spazio IPv4
- Circa 4,3 miliardi di indirizzi IPv4
- Espansione da 32 bit a 128 bit
- Numero teorico di indirizzi IPv6
- Riduzione della necessità del NAT

### 5.2 Struttura degli indirizzi IPv6
- Rappresentazione esadecimale
- Separazione tramite `:`
- Otto gruppi da quattro cifre esadecimali

### 5.3 Regole di compressione IPv6
- Rimozione degli zeri iniziali
- Compressione delle sequenze di gruppi nulli
- Utilizzo del simbolo `::`
- Limite di un solo utilizzo di `::`

### 5.4 Tipologie di indirizzi IPv6

#### 5.4.1 Unicast
- Identificazione di una singola interfaccia

##### Global Unicast
- Equivalente degli indirizzi IPv4 pubblici
- Instradamento attraverso Internet

##### Link-Local
- Generazione automatica
- Prefisso `fe80::`
- Validità limitata al segmento locale
- Utilizzo nei protocolli di routing
- Scoperta dei vicini

#### 5.4.2 Multicast
- Comunicazione verso gruppi di interfacce

#### 5.4.3 Anycast
- Stesso indirizzo assegnato a più dispositivi
- Instradamento verso il nodo più vicino

### 5.5 Configurazione IPv6 in Kathará
- Utilizzo di `iproute2`
- Assegnazione di un indirizzo:

  `ip -6 addr add <indirizzo>/<prefisso> dev <interfaccia>`

- Visualizzazione degli indirizzi:

  `ip -6 addr show`

- Configurazione della default route:

  `ip -6 route add default via <gateway>`

- Test della connettività:
  - `ping6`
  - `ping -6`


## 6. Neighbor Discovery Protocol e ARP *(pagg. 7-8)*

### 6.1 Neighbor Discovery Protocol — NDP
- Sostituzione di ARP in IPv6
- Utilizzo dei messaggi ICMPv6
- Comunicazione multicast
- Riduzione del traffico broadcast
- Stateless Address Autoconfiguration — SLAAC
- Autoconfigurazione degli indirizzi IPv6

### 6.2 Address Resolution Protocol — ARP
- Relazione tra livello rete e livello collegamento
- Indirizzi IP come indirizzi logici
- Indirizzi MAC come indirizzi fisici
- Associazione IP-MAC

### 6.3 Funzionamento del protocollo ARP

#### 6.3.1 ARP Request
- Invio in broadcast
- Ricerca del dispositivo associato a un indirizzo IP
- Inclusione del MAC del mittente

#### 6.3.2 ARP Reply
- Risposta in unicast
- Comunicazione dell’indirizzo MAC
- Costruzione del frame Ethernet

### 6.4 Cache ARP
- Memorizzazione temporanea delle associazioni IP-MAC
- Riduzione delle richieste ARP
- Timeout delle associazioni
- Aggiornamento della cache

### 6.5 Comandi per visualizzare la cache ARP
- `arp -n`
- `ip neigh show`

### 6.6 Analisi del traffico ARP con tcpdump
1. Pulizia della cache:

   `ip neigh flush all`

2. Avvio della cattura:

   `tcpdump -tenni eth0 arp`

3. Generazione del traffico tramite `ping`
4. Osservazione della sequenza:
   - ARP Request
   - ARP Reply
   - Pacchetti ICMP

### 6.7 Gratuitous ARP
- Invio spontaneo di una ARP Reply o Request
- Aggiornamento preventivo delle associazioni IP-MAC
- Segnalazione dei cambiamenti di indirizzo
- Rilevamento degli indirizzi IP duplicati

### 6.8 Proxy ARP
- Risposta ARP eseguita da un router per conto di un altro dispositivo
- Utilizzo del MAC del router
- Attrazione e successivo instradamento del traffico
- Possibili problemi di sicurezza


## 7. Protocollo OSPF — Open Shortest Path First *(pagg. 8-12)*

### 7.1 Introduzione a OSPF
- Interior Gateway Protocol
- Utilizzo in reti di grandi dimensioni
- Approccio Link State
- Differenze rispetto al Distance Vector

### 7.2 Costruzione della topologia
- Link State Update
- Meccanismo di flooding
- Propagazione degli aggiornamenti

### 7.3 Link State Database — LSDB
- Costruzione della mappa della rete
- Database identico su tutti i router

### 7.4 Algoritmo SPF
- Algoritmo di Dijkstra
- Calcolo autonomo dei percorsi
- Shortest Path Tree
- Router come radice dell’albero
- Prevenzione dei routing loop

### 7.5 Tipologie di messaggi OSPF
- Hello
  - Scoperta dei vicini
  - Mantenimento delle adiacenze
- Database Description — DBD/DD
  - Riassunto del database
- Link State Request — LSR
  - Richiesta degli LSA mancanti
- Link State Update — LSU
  - Invio degli aggiornamenti
- Link State Acknowledgment — LSAck
  - Conferma della ricezione

### 7.6 Indirizzi multicast OSPF
- `224.0.0.5`
  - Tutti i router OSPF
- `224.0.0.6`
  - Router designati

### 7.7 Metriche e costo OSPF
- Calcolo basato sul costo dei collegamenti
- Relazione con la larghezza di banda
- Formula di riferimento:

  `Cost = 10^8 / Bandwidth`

- Configurazione manuale del costo
- Comando `ospf cost`

### 7.8 Designated Router e Backup Designated Router

#### 7.8.1 Problema delle reti multi-accesso
- Numero elevato di adiacenze
- Crescita quadratica delle connessioni

#### 7.8.2 Designated Router — DR
- Centralizzazione dello scambio del database
- Adiacenze complete verso il DR

#### 7.8.3 Backup Designated Router — BDR
- Sostituzione del DR in caso di guasto

#### 7.8.4 Elezione del DR
- Priorità dell’interfaccia
- Priorità compresa tra 0 e 255
- Priorità 0: impossibilità di diventare DR
- Utilizzo del Router ID come criterio di spareggio
- Elezione non preemptive

### 7.9 Routing gerarchico e aree OSPF
- Riduzione del carico computazionale
- Suddivisione della rete in aree

#### 7.9.1 Area 0 — Backbone
- Area centrale
- Passaggio obbligatorio del traffico inter-area

#### 7.9.2 Internal Router
- Interfacce appartenenti alla stessa area
- Conoscenza completa dell’area locale

#### 7.9.3 Area Border Router — ABR
- Collegamento tra Area 0 e altre aree
- LSDB distinti per area
- Scambio di informazioni riassuntive

#### 7.9.4 Autonomous System Boundary Router — ASBR
- Importazione di rotte esterne
- Collegamento con altri protocolli

#### 7.9.5 Stub Area
- Riduzione delle informazioni esterne
- Filtraggio delle rotte BGP
- Distribuzione di una default route

### 7.10 Tipologie e priorità dei percorsi
Ordine di preferenza:

1. Intra-Area
2. Inter-Area
3. External Type 1 — E1
4. External Type 2 — E2

### 7.11 Convergenza e reazione ai guasti

#### 7.11.1 Link Fault
- Guasto dell’interfaccia
- Propagazione immediata degli LSA
- Ricalcolo della topologia

#### 7.11.2 Router Fault
- Rilevamento tramite mancati messaggi Hello
- RouterDeadInterval
- Intervallo predefinito di circa 40 secondi
- Aggiornamento delle tabelle
- Possibile nuova elezione del DR

### 7.12 Durata e aggiornamento degli LSA
- Refresh periodico
- MaxAge
- Persistenza temporanea delle informazioni

### 7.13 Tipologie di LSA

#### 7.13.1 Router LSA — Tipo 1
- Stato delle interfacce del router
- Link ID corrispondente al Router ID
- Comando:

  `show ip ospf database router`

#### 7.13.2 Network LSA — Tipo 2
- Generazione da parte del DR
- Rappresentazione delle reti multi-accesso
- Comando:

  `show ip ospf database network`

#### 7.13.3 Summary LSA
- Generazione da parte degli ABR
- Comunicazione delle reti presenti in altre aree
- Comando:

  `show ip ospf database summary`

#### 7.13.4 ASBR Summary LSA
- Indicazione dei percorsi verso gli ASBR

### 7.14 Equal-Cost Multi-Path — ECMP
- Installazione di più percorsi con costo uguale
- Inserimento di più rotte nella tabella
- Bilanciamento del traffico
- Ruolo del daemon Zebra
- Installazione delle rotte nel kernel Linux

### 7.15 Configurazione delle stub network
- OSPF attivo sull’interfaccia
- OSPF non attivo sull’interfaccia
- Redistribuzione come rotta esterna
- Configurazione dell’interfaccia passiva
- Soppressione dei pacchetti Hello
- Annuncio della rete nel dominio OSPF

### 7.16 Timer e convergenza sub-secondo
- Refresh LSA
- MaxAge
- DeadInterval
- SPF Throttle
- Riduzione degli Hello Timer
- Eliminazione o riduzione dello SPF Throttling
- BFD — Bidirectional Forwarding Detection
- Convergenza inferiore al secondo

### 7.17 Vantaggi e svantaggi di OSPF

#### Vantaggi
- Assenza del problema Count-to-Infinity
- Elevata scalabilità
- Ridotto traffico di segnalazione
- Supporto di metriche avanzate

#### Svantaggi
- Elevata complessità
- Necessità di progettazione accurata
- Configurazione più complessa rispetto a RIP


## 8. Linux Traffic Control — `tc` *(pagg. 12-13)*

### 8.1 Architettura di Traffic Control
- Tre componenti fondamentali:
  - Qdisc
  - Class
  - Filter

### 8.2 Queueing Discipline — qdisc
- Gestione delle code
- Ordine di trasmissione dei pacchetti

### 8.3 Class
- Suddivisione gerarchica delle qdisc
- Assegnazione di limiti di banda differenti

### 8.4 Filter
- Classificazione dei pacchetti
- Criteri:
  - Indirizzo IP
  - Porta
  - Protocollo

### 8.5 Principali qdisc

#### 8.5.1 PFIFO e BFIFO
- Code FIFO
- Limite per numero di pacchetti
- Limite in byte

#### 8.5.2 TBF — Token Bucket Filter
- Limitazione rigida della banda
- Modello del secchio di token
- Controllo della velocità di trasmissione

#### 8.5.3 HTB — Hierarchical Token Bucket
- Strutture gerarchiche
- Classi di traffico
- Banda garantita
- Utilizzo della banda inutilizzata
- Parametro `ceil`

#### 8.5.4 FQ-CoDel
- Fair Queueing
- Controlled Delay
- Riduzione del bufferbloat
- Gestione equa dei flussi
- Bassa latenza

#### 8.5.5 NetEm
- Emulazione di reti degradate
- Introduzione di:
  - Delay
  - Jitter
  - Packet loss
  - Corruzione
- Esempio:

  `tc qdisc add dev eth0 root netem delay 100ms loss 1%`

### 8.6 Gestione del traffico in ingresso
- Qdisc ingress
- Policing
- Eliminazione dei pacchetti oltre il limite
- Reazione del controllo di congestione TCP

### 8.7 Automazione e problematiche
- Perdita delle configurazioni dopo il riavvio
- Script di configurazione
- Utilizzo di wrapper Python
- Strumenti come `tcconfig`
- Rimozione delle vecchie qdisc:

  `tc qdisc del dev eth0 root`


## 9. Data Plane, Control Plane e inoltro IP *(pagg. 13-14)*

### 9.1 Data Plane
- Funzione di inoltro
- Forwarding dei pacchetti

### 9.2 Control Plane
- Funzione di instradamento
- Calcolo delle rotte

### 9.3 Implementazione del Control Plane

#### 9.3.1 Architettura per-router
- Algoritmi distribuiti
- Comunicazione tra router

#### 9.3.2 Controllo logicamente centralizzato
- Software Defined Networking
- Controller remoto
- Installazione delle regole negli switch

### 9.4 Inoltro diretto
- Verifica della subnet tramite AND logico
- Consegna diretta nella rete locale
- Risoluzione dell’indirizzo MAC

### 9.5 Inoltro indiretto
- Destinazione appartenente a una rete diversa
- Utilizzo del default gateway
- Invio al next-hop

### 9.6 Longest Prefix Match — LPM
- Ricerca della rotta più specifica
- Confronto tra prefissi CIDR
- Priorità alla maschera con più bit a 1
- Aggregazione delle rotte
- Riduzione delle dimensioni delle tabelle


## 10. Algoritmi di routing tradizionali *(pag. 14)*

### 10.1 Algoritmi Link State
- Conoscenza globale della topologia
- Distribuzione dello stato dei link
- Algoritmo di Dijkstra
- Calcolo dei cammini minimi
- Complessità computazionale
- Coerenza dei percorsi
- Prevenzione dei loop

### 10.2 Algoritmi Distance Vector
- Conoscenza dei soli vicini
- Algoritmo decentralizzato
- Aggiornamenti periodici
- Equazione di Bellman-Ford
- Count-to-Infinity
- Propagazione lenta delle informazioni negative
- Routing loop temporanei


## 11. Routing Internet e Autonomous System *(pag. 14)*

### 11.1 Autonomous System — AS
- Reti amministrate da un’unica organizzazione
- Suddivisione del routing Internet

### 11.2 Routing Intra-AS — IGP

#### RIP
- Algoritmo Distance Vector
- Hop count
- Limite di 15 salti
- Aggiornamenti UDP periodici

#### OSPF
- Protocollo Link State
- Algoritmo di Dijkstra
- Routing gerarchico
- Suddivisione in aree
- Backbone centrale

### 11.3 Routing Inter-AS — EGP

#### BGP — Border Gateway Protocol
- Protocollo fondamentale di Internet
- Approccio Path Vector
- Annuncio dell’intero AS-PATH
- Prevenzione dei loop
- Routing basato sulle policy
- Utilizzo di TCP
- Porta 179

#### eBGP
- Comunicazione tra Autonomous System differenti

#### iBGP
- Distribuzione delle rotte BGP all’interno dello stesso AS


## 12. Software Defined Networking e gestione della rete *(pag. 15)*

### 12.1 Software Defined Networking — SDN
- Separazione tra Data Plane e Control Plane
- Switch semplificati
- Centralizzazione dell’intelligenza

### 12.2 Controller SDN
- Networking Operating System
- Costruzione della mappa globale
- Controllo centralizzato e distribuito

### 12.3 Applicazioni di controllo
- Funzioni di gestione
- Traffic Engineering

### 12.4 Northbound API
- Comunicazione tra applicazioni e controller

### 12.5 Southbound API
- Comunicazione tra controller e switch
- OpenFlow

### 12.6 Gestione e configurazione della rete

#### SNMP
- Modello request-response
- Trap
- Management Information Base — MIB
- Monitoraggio dei dispositivi

#### NETCONF
- Configurazione automatizzata
- Scambio di dati XML
- Sessioni sicure

#### YANG
- Modellazione strutturata dei dati
- Configurazione dell’intera rete


## 13. Policy economiche e commerciali di Internet *(pagg. 15-16)*

### 13.1 Routing basato sulle policy
- Differenza tra routing IGP e BGP
- Prestazioni contro interessi economici
- Policy commerciali

### 13.2 Principio “No Free Transit”
- Evitare il trasporto gratuito del traffico

### 13.3 Relazione Provider-Customer
- Pagamento del provider
- Accesso a Internet
- Trasporto del traffico del cliente

### 13.4 Peering
- Scambio reciproco del traffico
- Assenza di pagamento diretto
- Beneficio reciproco

### 13.5 Stub Customer
- Cliente collegato a più provider
- Divieto di svolgere funzioni di transito
- Mancato annuncio delle rotte apprese da un provider all’altro

### 13.6 Provider “egoista”
- Mancata propagazione delle rotte
- Assenza di guadagno nel trasporto del traffico
- Applicazione delle policy BGP


## 14. Hot Potato Routing *(pag. 16)*

### 14.1 Principio di funzionamento
- Scelta del gateway di uscita più vicino
- Minimizzazione del costo interno
- Ignorare il costo successivo esterno

### 14.2 Obiettivi
- Riduzione dell’utilizzo delle risorse interne
- Trasferimento rapido del traffico a un altro AS


## 15. Protocollo BGP *(pagg. 17-20)*

### 15.1 Processo decisionale semplificato
Ordine iniziale dei criteri:

1. Local Preference
2. Shortest AS-PATH
3. Closest Next-Hop

### 15.2 Local Preference
- Attributo di policy
- Preferenza per clienti o provider
- Valore maggiore preferito

### 15.3 Shortest AS-PATH
- Scelta del percorso con meno AS attraversati

### 15.4 Closest Next-Hop
- Applicazione dell’Hot Potato Routing
- Scelta dell’uscita IGP più vicina

### 15.5 Configurazione dei vicini
- Configurazione esplicita dell’indirizzo IP
- Differenze rispetto ai protocolli IGP

### 15.6 Sessioni BGP
- Utilizzo di TCP
- Porta 179
- Annuncio dei prefissi
- Attributi dei percorsi

### 15.7 Stati della macchina a stati BGP
1. Idle
2. Connect
3. Active
4. OpenSent
5. OpenConfirm
6. Established

### 15.8 Messaggi di apertura
- Numero di AS
- BGP Router ID
- Hold Time
- Keepalive

### 15.9 Configurazione eBGP con FRRouting
- Avvio del processo BGP:

  `router bgp <AS>`

- Configurazione del vicino:

  `neighbor <IP> remote-as <AS>`

- Verifica:

  `show ip bgp neighbors`

- Annuncio di una rete:

  `network <prefisso>`

### 15.10 Policy predefinite di FRRouting
- Blocco degli annunci eBGP senza policy
- Comando:

  `no bgp ebgp-requires-policy`

- Verifica della presenza locale della rete
- Network import check

### 15.11 Filtraggio degli annunci

#### Prefix-List
- Permesso o blocco dei prefissi
- Regole numerate
- Numeri di sequenza
- Deny implicito finale

#### AS-Path Access-List
- Filtraggio degli AS attraversati
- Espressioni regolari

### 15.12 Attributi BGP e Best-Path

#### Weight
- Attributo proprietario Cisco
- Valore locale al router

#### Local Preference
- Condivisione tramite iBGP
- Selezione dell’uscita preferita
- Valore più alto preferito

#### Originate
- Preferenza per le rotte generate localmente

#### AS-Path Length
- Numero di AS attraversati
- Prevenzione dei loop
- Percorso più corto preferito

#### AS-Path Prepending
- Ripetizione artificiale del proprio ASN
- Penalizzazione di un percorso

#### Origin Code
- IGP
- EGP
- Incomplete

#### MED — Multi Exit Discriminator
- Indicazione del collegamento preferito per il traffico di ritorno
- Attributo opzionale e non transitivo
- Valore minore preferito

### 15.13 Route-Map
- Modello match/set
- Modifica degli attributi
- Applicazione in ingresso
- Applicazione in uscita

Esempi:

`match ip address <ACL>`

`set metric <valore>`

`set local-preference <valore>`

### 15.14 Next-Hop e Recursive Lookup
- Persistenza del Next-Hop in iBGP
- Necessità di raggiungere il Next-Hop tramite IGP
- Recursive Lookup
- Problemi di raggiungibilità
- Comando:

  `next-hop-self`

### 15.15 Stub Network e Default Route
- AS cliente collegato a un solo provider
- Mancata necessità della tabella Internet completa
- Distribuzione di `0.0.0.0/0`
- Comando BGP `network 0.0.0.0/0`
- Comando `default-originate`

### 15.16 Multi-Homed Stub Network
- Collegamenti ridondanti
- Policy primario/backup
- Failover tramite BGP

#### Controllo del traffico inbound
- Utilizzo del MED
- Metrica maggiore sul collegamento di backup

#### Controllo del traffico outbound
- Modifica della Local Preference
- Penalizzazione del percorso di backup

### 15.17 Load Sharing tra provider
- Annuncio del prefisso aggregato
- Suddivisione in prefissi più specifici
- Utilizzo del Longest Prefix Match
- Distribuzione del traffico tra ISP
- Rotta aggregata come fallback


## 16. BGP nei Data Center *(pagg. 20-21)*

### 16.1 Architetture Clos e Fat-Tree
- Esigenze delle applicazioni cloud
- Traffico est-ovest
- Microservizi
- Abbandono delle topologie gerarchiche tradizionali

### 16.2 Strati degli switch

#### Leaf
- Collegamento ai server

#### Spine
- Collegamento agli switch Leaf

#### Top of Fabric — ToF
- Aggregazione dell’infrastruttura
- Organizzazione in Point of Delivery — PoD

### 16.3 Vantaggi delle reti Fat-Tree
- Percorsi multipli
- Percorsi di uguale lunghezza
- Elevata banda
- Ridondanza
- Resistenza ai guasti

### 16.4 ECMP e BGP
- Utilizzo di BGP al posto di OSPF
- Minore traffico di flooding
- Supporto Equal-Cost Multi-Path
- Bilanciamento tramite hashing nel kernel

### 16.5 Assegnazione degli Autonomous System
- Utilizzo di ASN privati
- ASN distinti per gli switch Leaf
- ASN condivisi tra gli Spine
- Organizzazione degli ASN dei ToF

### 16.6 BGP Multi-Path Relax
- Problema degli AS-PATH differenti
- Comando/funzione:

  `bgp bestpath as-path multipath-relax`

- Confronto basato sulla sola lunghezza del percorso

### 16.7 Multi-Path Traceroute
- Limiti del traceroute tradizionale
- Risultati incoerenti in presenza di ECMP
- Paris-Traceroute
- Dublin-Traceroute
- Ricostruzione dei diversi percorsi

### 16.8 Ottimizzazione dei timer BGP nei Data Center
- Advertisement Interval a 0 secondi
- Aggiornamenti immediati
- Keepalive ridotto
- Hold Timer ridotto
- Connect Timer ridotto
- Riconnessione rapida dei peer


## 17. Livello di trasporto *(pag. 21)*

### 17.1 Obiettivi del livello di trasporto
- Collegamento tra livello applicativo e livello rete
- Comunicazione tra processi

### 17.2 Multiplexing
- Raccolta dei dati dalle applicazioni
- Aggiunta delle porte
- Creazione dei segmenti
- Consegna al livello IP

### 17.3 Demultiplexing
- Analisi della porta di destinazione
- Consegna al processo corretto

### 17.4 Numeri di porta
- Identificazione delle applicazioni
- Smistamento dei segmenti

### 17.5 Socket UDP
Identificazione tramite:
- Indirizzo IP locale
- Porta locale

### 17.6 Socket TCP
Identificazione tramite:
- IP locale
- Porta locale
- IP remoto
- Porta remota

### 17.7 Affidabilità sopra una rete inaffidabile
- Perdita dei pacchetti
- Riordinamento
- Corruzione
- Congestione


## 18. Reliable Data Transfer — RDT *(pagg. 22-23)*

### 18.1 Gestione dei dati corrotti

#### Checksum
- Calcolo di un valore di controllo
- Inserimento nell’header
- Ricalcolo lato ricevente
- Rilevamento della corruzione

#### ACK
- Conferma positiva

#### NACK
- Segnalazione di dati corrotti
- Richiesta di ritrasmissione

### 18.2 Corruzione degli ACK

#### Sequence Number
- Numerazione progressiva
- Identificazione dei duplicati
- Ritrasmissione di sicurezza
- Eliminazione della necessità dei NACK

### 18.3 Gestione della perdita
- Timer
- Timeout
- Presunzione della perdita
- Ritrasmissione

### 18.4 Stop-and-Wait
- Attesa dell’ACK prima dell’invio successivo
- Affidabilità
- Scarsa utilizzazione della banda

### 18.5 Pipelining
- Invio di più pacchetti consecutivi
- Sliding Window
- Miglioramento dell’utilizzo della rete

### 18.6 Go-Back-N
- ACK cumulativi
- Rifiuto dei pacchetti fuori ordine
- Timeout
- Ritrasmissione del pacchetto perso e dei successivi

### 18.7 Selective Repeat
- ACK indipendenti
- Buffer lato ricevente
- Memorizzazione dei pacchetti fuori ordine
- Ritrasmissione del solo pacchetto mancante


## 19. Fondamenti del protocollo TCP *(pagg. 23-24)*

### 19.1 Meccanismi di affidabilità
- Checksum
- ACK cumulativi
- Sequence Number
- Numerazione dei byte
- Timeout
- Ritrasmissioni

### 19.2 Instaurazione della connessione
- Three-Way Handshake
- Flag SYN
- Flag ACK

### 19.3 Flow Control
- Protezione del ricevitore
- Controllo della quantità di dati in transito

### 19.4 Congestion Control
- Protezione della rete
- Congestion Window — `cwnd`

### 19.5 Self-Clocking
- ACK come indicatore della disponibilità della rete
- Aumento della finestra alla ricezione degli ACK
- Riduzione della finestra in caso di perdita

### 19.6 TCP Tahoe e TCP Reno

#### Slow Start
- Finestra iniziale di 1 MSS
- Crescita esponenziale
- Raddoppio della finestra a ogni RTT

#### Congestion Avoidance
- Soglia `ssthresh`
- Crescita lineare
- Incremento di circa 1 MSS per RTT

### 19.7 Rilevamento delle perdite

#### Timeout
- Danno grave
- Riduzione di `ssthresh`
- Ripristino della finestra a 1 MSS
- Ripartenza tramite Slow Start

#### Tre ACK duplicati
- Identificazione di una perdita isolata
- Fast Retransmit
- Fast Recovery
- Riduzione della finestra
- Ripresa dalla crescita lineare


## 20. TCP CUBIC *(pagg. 24 e 26)*

### 20.1 Limiti di TCP Reno
- Prestazioni ridotte su reti veloci
- Elevata latenza
- Bandwidth-Delay Product elevato

### 20.2 Funzione cubica
- Crescita basata sul tempo
- Indipendenza dall’RTT
- Ricerca del limite di capacità

### 20.3 Fasi della curva CUBIC

#### Concave Region
- Fast Recovery
- Crescita rapida
- Avvicinamento a `Wmax`

#### Plateau Region
- Crescita prudente
- Verifica della stabilità della rete

#### Convex Region
- Ricerca aggressiva di nuova banda
- Superamento di `Wmax`

### 20.4 Modalità TCP-Friendly
- Compatibilità con TCP Reno
- Riduzione delle penalizzazioni sui collegamenti lenti


## 21. Protocollo QUIC e HTTP/3 *(pagg. 24-25)*

### 21.1 Introduzione a QUIC
- Protocollo sviluppato da Google
- Base di HTTP/3
- Implementazione sopra UDP
- Esecuzione in user space
- Aggiornamento indipendente dal kernel

### 21.2 Velocità di instaurazione
- Riduzione dei round-trip
- Fusione tra handshake e TLS
- Supporto 0-RTT

### 21.3 Flussi indipendenti
- Multiplexing
- Eliminazione dell’Head-of-Line Blocking tra stream
- Continuazione degli altri flussi in caso di perdita

### 21.4 Sicurezza integrata
- TLS 1.3 obbligatorio
- Assenza di connessioni non cifrate

### 21.5 Connection Migration
- Identificativo di connessione indipendente dall’IP
- Passaggio tra Wi-Fi e rete mobile
- Continuità delle sessioni


## 22. Controllo della congestione e Fairness *(pagg. 25-27)*

### 22.1 Obiettivi del controllo di congestione
- Prevenzione del congestion collapse
- Riduzione del traffico inutile
- Utilizzo efficiente delle risorse

### 22.2 Efficienza ed equità
- Massimizzazione del throughput
- Efficienza paretiana
- Rischio di penalizzazione dei flussi
- Compromesso tra efficienza e fairness

### 22.3 Modelli di Fairness

#### Max-Min Fairness
- Massimizzazione delle velocità minime
- Distribuzione equa della banda
- Bottleneck link
- Algoritmo di Water Filling

#### Proportional Fairness
- Massimizzazione della somma dei logaritmi
- Bilanciamento tra efficienza ed equità
- Penalizzazione dei flussi più costosi

#### Utility Fairness
- Massimizzazione della funzione di utilità
- Considerazione dei costi della rete
- Generalizzazione della Max-Min Fairness

### 22.4 Algoritmo AIMD
- Additive Increase
- Multiplicative Decrease
- Crescita additiva in assenza di congestione
- Riduzione moltiplicativa in caso di congestione
- Convergenza verso un punto equo

### 22.5 Analisi tramite equazioni differenziali
- Modellazione tramite ODE
- Code FIFO
- Bias nei confronti delle connessioni con RTT elevato

### 22.6 Variabili del controllo TCP
- Congestion Window — `cwnd`
- Target Window
- Slow Start Threshold — `ssthresh`

### 22.7 Evoluzioni moderne

#### TCP CUBIC
- Crescita cubica
- Indipendenza dall’RTT

#### Data Center TCP — DCTCP
- Reti a bassissima latenza
- Congestione proporzionale
- Stima della probabilità di congestione
- Riduzione proporzionale della finestra
- Throughput elevato e stabile


## 23. Active Queue Management ed ECN *(pag. 27)*

### 23.1 Bufferbloat
- Accumulo eccessivo di pacchetti
- Elevata latenza
- Limiti del Tail Drop

### 23.2 RED — Random Early Detection
- Active Queue Management
- Eliminazione anticipata dei pacchetti
- Scarto probabilistico
- Utilizzo della lunghezza media della coda
- Prevenzione della saturazione del buffer

### 23.3 ECN — Explicit Congestion Notification
- Segnalazione esplicita della congestione
- Marcatura dei pacchetti
- Modifica dei bit nell’header IP
- Flag TCP ECE
- Riduzione della finestra senza perdita effettiva


## 24. Isolamento e classificazione del traffico *(pag. 27)*

### 24.1 Applicazioni TCP-Friendly
- Applicazioni audio e video basate su UDP
- Condivisione equa della banda
- Algoritmi TFRC
- Loss-Throughput Formula
- Compatibilità con i flussi TCP

### 24.2 Class-Based Queueing
- Separazione dei flussi in classi
- Limitazione del traffico UDP aggressivo
- Code con pesi differenti

### 24.3 Weighted Fair Queueing
- Allocazione pesata della banda
- Isolamento dei flussi
- Garanzia di una banda minima
- Protezione delle applicazioni concorrenti