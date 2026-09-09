# OSPF II - soluzione eseguibile e ripasso rapido

Questa cartella contiene lo scenario OSPF multi-area principale. Gli scenari
incompatibili sono indipendenti:

- `backbone-rip/`: RIP sul backbone, OSPF nelle aree periferiche;
- `asbr-bgp/`: AS10/AS100, stub no-summary e rotta esterna E2.

La topologia e gli indirizzi provengono dalla figura e dai file ufficiali
`kathara-lab_ospf_frr-multiarea` e `kathara-lab_ospf_frr-complex`, conservati
nella cronologia Git della repository. Il markdown originale non è stato
modificato.

## 1. Schema della topologia

```text
Area 1.1.1.1 (stub)                  Area 2.2.2.2 (stub)
200.0.1/24--r2--200.0.0/30--r1       210.0.0/24--r3
                         |                       / \
                    100.0.0/30          110.0.0/30 120.0.0/30
                         |                 /             \
                        bb1--------------/              bb2
                         |                                |
                 +-------+---- Area 0 ----+---------------+
                 | bb0, bb1, bb2, bb3, bb4 |
                 +--------------------------+
                                                          |
                                                     130.0.0/30
                                                          |
Area 3.3.3.3 (stub)                           r4-----r5-----r6
                                      reti 220.0.0/30, .1/30, .2/30
```

Collision domain backbone: A=`10.0.0.0/24`, B=`10.0.1.0/24`,
C=`10.0.2.0/24`, D=`10.0.3.0/24`. I domini E-I collegano gli ABR alle
aree; J e K sono LAN terminali; L-N formano il triangolo dell'area 3.

## 2. Matrice router/interfacce

`auto` significa costo automatico FRR: la fonte ufficiale imposta
esplicitamente solo 90 e 100. Nel test con `kathara/frr:latest` del
09/09/2026 il costo automatico osservato è 10; controllarlo comunque con
`show ip ospf interface` se si usa un'immagine diversa.

| Router | Eth | IP/prefix | Subnet | CD | Area | Costo | Ruolo |
|---|---:|---|---|---|---|---:|---|
| bb0 | 0 | 10.0.0.3/24 | 10.0.0.0/24 | A | 0.0.0.0 | auto | internal, backbone |
| bb0 | 1 | 10.0.2.3/24 | 10.0.2.0/24 | C | 0.0.0.0 | auto | internal, backbone |
| bb1 | 0 | 10.0.0.1/24 | 10.0.0.0/24 | A | 0.0.0.0 | 90 | ABR, backbone |
| bb1 | 1 | 10.0.3.1/24 | 10.0.3.0/24 | D | 0.0.0.0 | auto | ABR, backbone |
| bb1 | 2 | 100.0.0.1/30 | 100.0.0.0/30 | E | 1.1.1.1 | auto | ABR |
| bb1 | 3 | 110.0.0.1/30 | 110.0.0.0/30 | F | 2.2.2.2 | auto | ABR |
| bb2 | 0 | 10.0.0.2/24 | 10.0.0.0/24 | A | 0.0.0.0 | 100 | ABR, backbone |
| bb2 | 1 | 10.0.1.1/24 | 10.0.1.0/24 | B | 0.0.0.0 | auto | ABR, backbone |
| bb2 | 2 | 130.0.0.1/30 | 130.0.0.0/30 | H | 3.3.3.3 | auto | ABR |
| bb2 | 3 | 120.0.0.1/30 | 120.0.0.0/30 | G | 2.2.2.2 | auto | ABR |
| bb3 | 0 | 10.0.1.2/24 | 10.0.1.0/24 | B | 0.0.0.0 | auto | internal, backbone |
| bb3 | 1 | 10.0.2.2/24 | 10.0.2.0/24 | C | 0.0.0.0 | auto | internal, backbone |
| bb4 | 0 | 10.0.2.1/24 | 10.0.2.0/24 | C | 0.0.0.0 | auto | internal, backbone |
| bb4 | 1 | 10.0.3.2/24 | 10.0.3.0/24 | D | 0.0.0.0 | auto | internal, backbone |
| r1 | 0 | 100.0.0.2/30 | 100.0.0.0/30 | E | 1.1.1.1 | auto | internal |
| r1 | 1 | 200.0.0.1/30 | 200.0.0.0/30 | I | 1.1.1.1 | auto | internal |
| r2 | 0 | 200.0.0.2/30 | 200.0.0.0/30 | I | 1.1.1.1 | auto | internal |
| r2 | 1 | 200.0.1.1/24 | 200.0.1.0/24 | J | 1.1.1.1 | auto | internal |
| r3 | 0 | 120.0.0.2/30 | 120.0.0.0/30 | G | 2.2.2.2 | auto | internal |
| r3 | 1 | 110.0.0.2/30 | 110.0.0.0/30 | F | 2.2.2.2 | auto | internal |
| r3 | 2 | 210.0.0.1/24 | 210.0.0.0/24 | K | 2.2.2.2 | auto | internal |
| r4 | 0 | 220.0.0.1/30 | 220.0.0.0/30 | L | 3.3.3.3 | auto | internal |
| r4 | 1 | 220.0.1.1/30 | 220.0.1.0/30 | N | 3.3.3.3 | auto | internal |
| r5 | 0 | 220.0.2.2/30 | 220.0.2.0/30 | M | 3.3.3.3 | auto | internal |
| r5 | 1 | 220.0.1.2/30 | 220.0.1.0/30 | N | 3.3.3.3 | auto | internal |
| r5 | 2 | 130.0.0.2/30 | 130.0.0.0/30 | H | 3.3.3.3 | auto | internal |
| r6 | 0 | 220.0.0.2/30 | 220.0.0.0/30 | L | 3.3.3.3 | auto | internal |
| r6 | 1 | 220.0.2.1/30 | 220.0.2.0/30 | M | 3.3.3.3 | auto | internal |

Ogni /30 ha esattamente due endpoint. Gli unici segmenti multiaccess con più
di due router sono A (bb0, bb1, bb2) e C (bb0, bb3, bb4).

## 3. Avvio e controlli

```sh
cd LAB_RIP_II_OSPF/OSPF_II
kathara lstart
# attendere circa 45 s per la convergenza iniziale
./check.sh
kathara lclean
```

Comandi diagnostici, dentro un router o tramite `kathara exec`:

```sh
vtysh -c "show ip ospf neighbor"
vtysh -c "show ip ospf interface"
vtysh -c "show ip ospf route"
vtysh -c "show ip ospf database"
vtysh -c "show ip ospf database router"
vtysh -c "show ip ospf database summary"
vtysh -c "show ip route"
```

## 4. Q0-Q12

### Q0 - ABR e raggiungibilità da una stub area

**Router/comando:** `bb1`, `vtysh -c "show ip ospf"`; `r2`,
`vtysh -c "show ip ospf route"`.

**Atteso:** bb1 risulta ABR perché ha interfacce in area 0, 1 e 2. Su r2
compare `N IA 0.0.0.0/0`, oltre alle rotte intra-area e ai Summary Type 3
consentiti da una stub standard.

**Spiegazione:** un Area Border Router collega una o più aree non-backbone
all'area 0 e mantiene una LSDB distinta per ciascuna. Una stub area non riceve
Type 5 esterni; l'ABR le origina una default Type 3. Il router interno inoltra
le destinazioni non note verso l'ABR.

**Orale:** “L'ABR appartiene al backbone e a un'altra area, mantiene più
LSDB e traduce la raggiungibilità fra aree tramite Summary LSA. Nella stub gli
esterni sono sostituiti da una default verso l'ABR.”

### Q1 - `show ip ospf database summary`

**Router/comando:** `r2` e `bb1`:

```sh
vtysh -c "show ip ospf database summary"
```

**Atteso:** record `Summary Link States` con LS type `summary-LSA`, Link State
ID uguale alla rete riassunta, Advertising Router uguale all'ABR e `Metric`.
Nella stub standard r2 vede anche il Summary Type 3 per `0.0.0.0/0`.

**Spiegazione:** le Type 3 sono generate dagli ABR per annunciare in un'area
reti appartenenti ad altre aree. Evitano di copiare la topologia completa: il
router conosce prefisso, ABR e distanza dall'ABR, non tutti i link esterni.

**Orale:** “Mostra le Type 3 prodotte dagli ABR: raggiungibilità inter-area e
metrica dall'ABR alla destinazione.”

### Q2 - `show ip ospf route`, O e O IA

**Router/comando:** `r2`, `vtysh -c "show ip ospf route"`; poi
`vtysh -c "show ip route"`.

**Atteso:** nella tabella OSPF FRR le reti locali sono `N` intra-area e quelle
esterne all'area sono `N IA`; nella tabella globale diventano `O` e `O IA`.
Per esempio `100.0.0.0/30` è intra-area su r2, mentre reti backbone/periferiche
sono inter-area.

**Spiegazione:** `O` deriva dalla SPF sulla LSDB dell'area locale; `O IA`
deriva da Type 3 e dal costo locale per raggiungere l'ABR.

**Orale:** “O è intra-area e usa la topologia completa locale; O IA è
inter-area e usa un Summary LSA dell'ABR.”

### Q3 - neighbor e LSDB separate

**Router/comando:** tutti, `vtysh -c "show ip ospf neighbor"`.

| Router | Neighbor attesi |
|---|---:|
| bb0 | 4: bb1, bb2, bb3, bb4 |
| bb1 | 5: bb0, bb2, bb4, r1, r3 |
| bb2 | 5: bb0, bb1, bb3, r3, r5 |
| bb3 | 3: bb2, bb0, bb4 |
| bb4 | 3: bb0, bb3, bb1 |
| r1 | 2: bb1, r2 |
| r2 | 1: r1 |
| r3 | 2: bb1, bb2 |
| r4 | 2: r5, r6 |
| r5 | 3: bb2, r4, r6 |
| r6 | 2: r4, r5 |

Su Ethernet multiaccess una coppia di DROther può restare `2-Way`; non è un
errore. DR/BDR e Router ID dipendono anche dall'ordine di avvio.

**Spiegazione:** un'adiacenza appartiene sempre a una sola area e i due lati
del link devono concordare sull'Area ID. L'ABR non fonde le LSDB: esegue SPF
separata e origina Type 3 verso le altre aree.

**Orale:** “Non esiste una LSDB globale multi-area: ogni area ha la propria;
l'ABR conserva più LSDB e scambia raggiungibilità riassunta.”

### Q4 - traceroute bb0-r2 e ritorno

**Router/comandi:**

```sh
kathara exec bb0 -- traceroute -n 200.0.0.2
kathara exec r2 -- traceroute -n 10.0.2.3
```

**Atteso:** andata `bb0 -> bb1 -> r1 -> r2`. Il traffico attraversa area 0,
ABR bb1 e area 1. Il ritorno verso l'indirizzo C di bb0 è normalmente
`r2 -> r1 -> bb1 -> bb4 -> bb0`: il costo 90 in uscita da `bb1 eth0` rende
più conveniente D-C. Le risposte ICMP possono mostrare indirizzi diversi
dello stesso router, ma non cambia la sequenza logica.

**Costo:** andata = costo bb0→bb1 + costo bb1→r1→r2. Ritorno = costo
r2→r1→bb1 + min(`bb1 eth0`=90 più bb0→C, bb1→D→bb4→C). OSPF usa costi
direzionali, quindi l'asimmetria è prevista.

**Orale:** “L'ABR è bb1. L'andata usa il collegamento diretto A; il ritorno
evita l'uscita a costo 90 di bb1 e passa da bb4.”

### Q5 - più LSDB sull'ABR

**Router/comando:** `bb1`, `vtysh -c "show ip ospf database router"`.

**Atteso:** tre sezioni `Router Link States`: area 0.0.0.0, area 1.1.1.1
[Stub] e area 2.2.2.2 [Stub]. La domanda ne confronta due, ma bb1 appartiene
in realtà a tre aree.

**Spiegazione:** in ogni area sono comuni e sincronizzate Type 1/2 solo fra i
router di quell'area. Sequenze, flooding e SPF sono separati. Fra aree passa
la raggiungibilità Type 3, non la topologia dettagliata.

**Orale:** “bb1 ha tre LSDB indipendenti, una per area; condivide dentro ogni
area Type 1/2, mentre fra aree genera Type 3.”

### Q6 - modifica costo e riconvergenza

**Router/comandi esatti:** su bb0:

```sh
vtysh
configure terminal
interface eth0
 ospf cost 50
end
write memory
```

Monitorare contemporaneamente:

```sh
kathara exec bb0 -- watch -n 0.2 'traceroute -n -m 8 200.0.0.2'
kathara exec bb1 -- vtysh -c "show ip ospf database router"
```

**Atteso:** il percorso bb0→r2 può passare da `bb0-bb4-bb1-r1-r2` invece
del link A diretto. bb0 origina una nuova Type 1 in area 0; flooding, SPF e
RIB/FIB seguono. Ripristino: `interface eth0`, `no ospf cost`, `write memory`.

**Precisazione importante:** il testo chiede di osservare da r2, ma il costo
è quello *in uscita* da bb0; il percorso r2→bb0 può quindi non cambiare.
L'esperimento osservabile è bb0→r2. Inoltre i Summary LSA cambiano solo se
cambia la distanza calcolata dall'ABR alla rete riassunta: questa modifica
può cambiare SPF e next hop senza cambiare la metrica Type 3 originata da bb1.

**Misura:** annotare il tempo del primo traceroute col nuovo next hop e
sottrarre l'istante del comando. Una modifica locale di costo viene segnalata
subito, quindi è normalmente nell'ordine dei secondi, non del Dead Timer.

**Orale:** “Cambio costo → nuova Router LSA Type 1 → flooding nell'area 0 →
SPF → RIB/FIB. Le Type 3 si aggiornano solo se varia la metrica dell'ABR.”

### Q7 - aree, router e metriche Summary

**Aree:** 0.0.0.0 backbone; 1.1.1.1, 2.2.2.2 e 3.3.3.3 stub.

- Internal router: bb0, bb3, bb4, r1, r2, r3, r4, r5, r6.
- Backbone router: bb0, bb1, bb2, bb3, bb4.
- ABR: bb1 (0/1/2) e bb2 (0/2/3).
- ASBR nello scenario base: nessuno.

**Router/comando:** `r2`, `r3`, `r5`,
`vtysh -c "show ip ospf database summary"`.

**Atteso/spiegazione:** `Metric` nella Type 3 è il costo dell'ABR dalla
propria posizione alla destinazione annunciata; il ricevente aggiunge il
proprio costo intra-area fino all'ABR. Se si configura un range, la metrica
del summary è il massimo dei componenti.

**Orale:** “bb1 e bb2 sono ABR; ogni Type 3 porta la distanza dall'ABR, alla
quale il router interno somma il costo per raggiungere quell'ABR.”

### Q8 - default nella stub area

**Router/comando:** `r2`, `vtysh -c "show ip ospf route"`.

**Atteso:** `N IA 0.0.0.0/0 [21] ... via r1`; nella tabella globale
`O>* 0.0.0.0/0 [110/21]`. La metrica è
`costo(r2→r1→bb1) + stub default-cost 1`: nel runtime verificato sono due
link da 10 più la metrica Type 3 pari a 1. Su r3, direttamente connesso a
entrambi gli ABR, la default è ECMP con costo 11.

**Spiegazione:** bb1 origina la Type 3 default. Riduce LSDB e tabella, e
nasconde tutte le rotte esterne che una stub non può ricevere.

**Orale:** “La default è una Summary Type 3 dell'ABR, metrica iniziale 1 più
il costo locale fino all'ABR; qui r2 totalizza 21.”

### Q9 - spegnimento link ABR-stub

**Router/comandi:** su bb1:

```sh
ip link set dev eth2 down
vtysh -c "show ip ospf neighbor"
# ripristino
ip link set dev eth2 up
```

Su r1/r2 monitorare neighbor, route e summary.

**Atteso:** scompare l'adiacenza bb1-r1. Su bb1 la notifica locale è
immediata; r1, se non riceve carrier-down, scade dopo il Dead Timer (default
circa 40 s). Cambiano le Type 1 dell'area 1 e la default Type 3 di bb1 non è
più utilizzabile da r1/r2. Non esiste un ABR alternativo per area 1, quindi
non appare una nuova default e non c'è percorso alternativo verso il
backbone; r1-r2 restano adiacenti e conservano la connettività interna.

**Orale:** “Area 1 ha un solo ABR: down di bb1-eth2 isola la stub. Locale è
immediato; dall'altro lato può servire il Dead Timer.”

### Q10 - perdita sul link ABR-stub

**Router/comandi corretti:** il link area 1 è `bb1 eth2`, non eth1.

```sh
tc qdisc add dev eth2 root netem loss 1%
tc qdisc change dev eth2 root netem loss 5%
tc qdisc change dev eth2 root netem loss 30%
tc qdisc del dev eth2 root
```

**Atteso:** 1% e 5% causano perdita dati ma raramente quattro Hello OSPF
consecutivi; neighbor e LSDB dovrebbero restare stabili. A perdite elevate
possono scadere i Dead Timer: neighbor `Full→Down`, ricalcolo SPF, perdita
della default e successiva risincronizzazione LSDB (`ExStart/Exchange/Loading`
prima di `Full`). Con loss casuale la convergenza dipende dai timer; con
`ip link down` la notifica locale è deterministica e immediata.

**Orale:** “Netem loss non equivale a link-down: finché arrivano Hello entro
il Dead Interval l'adiacenza resta Full; solo perdite consecutive provocano
flap e nuova sincronizzazione.”

### Q11 - stub no-summary

Scenario: `cd asbr-bgp && kathara lstart`.

**Configurazione:** sull'ABR bb1 `area 1.1.1.1 stub no-summary`; su r1/r2
rimane `area 1.1.1.1 stub`. Il `no-summary` va solo sull'ABR.

**Router/comandi:** r2 e bb1:

```sh
vtysh -c "show ip ospf database summary"
vtysh -c "show ip ospf database asbr-summary"
vtysh -c "show ip ospf route"
```

**Atteso su r2:** Type 3 dettagliate assenti; presente solo Type 3
`0.0.0.0/0`; Type 4 ASBR-summary assenti; Type 5 assenti; nessuna rotta
inter-area specifica, solo default. Nell'ABR, la LSDB area 1 rispetta gli
stessi filtri; nelle altre sue LSDB restano le informazioni consentite.

**Stub vs no-summary:** una stub standard blocca Type 4/5 ma accetta Type 3
inter-area più default. Una stub no-summary (“totally stubby”, estensione
vendor) blocca anche le Type 3 specifiche e lascia soltanto la default.

**Orale:** “No-summary sull'ABR sopprime anche le Type 3 inter-area; dentro
restano topologia locale e default.”

### Q12 - 50.0.0.0/16 esterna E2

Scenario: `asbr-bgp/`. `as100r1` AS100 annuncia 50.0.0.0/16 a bb3 AS10;
bb3 è l'ASBR OSPF e usa `redistribute bgp metric-type 2 metric 20`.

**Router/comandi:**

```sh
# backbone
kathara exec bb1 -- vtysh -c "show ip ospf database external"
kathara exec bb1 -- vtysh -c "show ip route 50.0.0.0/16"
kathara exec bb1 -- ping -c 3 50.0.0.1
kathara exec bb1 -- traceroute -n 50.0.0.1

# internal router della totally stubby area 1
kathara exec r2 -- vtysh -c "show ip ospf database external"
kathara exec r2 -- vtysh -c "show ip route"
kathara exec r2 -- ping -c 3 50.0.0.1
kathara exec r2 -- traceroute -n 50.0.0.1
```

**Atteso:** bb1 vede una Type 5 per 50.0.0.0/16, advertising router bb3, e
una route `O E2 ... [110/20]`. E2 conserva metrica esterna 20; il costo OSPF
fino all'ASBR rompe solo eventuali pareggi. r2 non vede Type 5 né una rotta
50/16 specifica: usa la default Type 3 verso bb1. Ping e traceroute devono
comunque riuscire passando `r2-r1-bb1-(backbone)-bb3-as100r1`.

**Orale:** “bb3 redistribuisce BGP e origina la Type 5 E2. La Type 5 non entra
nella stub; r2 raggiunge 50/16 con la default dell'ABR.”

## 5. Scenario backbone RIP

Avvio separato:

```sh
cd backbone-rip
kathara lstart
./check.sh
kathara lclean
```

RIP v2 gira su bb0-bb4. bb1 e bb2 fanno da confine di redistribuzione:
annunciano in RIP rotte connesse/OSPF e redistribuiscono le rotte RIP in OSPF
come E2 metric 10. Non esiste più un'area 0 OSPF.

Conseguenze concrete nelle LSDB periferiche:

- spariscono i Summary Type 3 generati dagli ABR attraverso area 0;
- non può attraversare RIP alcuna LSA: RIP scambia distance vector, non LSDB;
- bb1/bb2 non sono più ABR OSPF nel senso standard, ma boundary router/ASBR;
- le aree periferiche non possono restare stub se devono ricevere le Type 5
  della redistribuzione: sono quindi aree normali nello scenario;
- le destinazioni esterne all'area sono apprese come rotte E2 specifiche,
  mentre le reti periferiche sono importate nel dominio RIP.

Questa è anche la risposta alla seconda “Question 1” del testo: la richiesta
di conservare contemporaneamente stub OSPF, Type 5 di redistribuzione e un
backbone non OSPF è incompatibile con la semantica standard delle stub area.

## 6. LSA e path type nella topologia

| Tipo | Nome | Origine/scopo | Presenza |
|---:|---|---|---|
| 1 | Router LSA | ogni router descrive i propri link nell'area | tutte le aree |
| 2 | Network LSA | il DR descrive un segmento multiaccess | dove eletto DR |
| 3 | Summary LSA | ABR annuncia prefissi inter-area/default stub | base e default in stub |
| 4 | ASBR Summary | ABR indica come raggiungere un ASBR di altra area | non entra nelle stub |
| 5 | AS External | ASBR annuncia 50.0.0.0/16 | area 0 di `asbr-bgp`, non stub |

| Path | Significato | Metrica/preferenza |
|---|---|---|
| O | intra-area | SPF della LSDB locale; preferito |
| O IA | inter-area | costo fino ad ABR + Summary Type 3 |
| O E1 | esterno tipo 1 | metrica esterna + costo interno fino ASBR |
| O E2 | esterno tipo 2 | metrica esterna; costo fino ASBR come tie-break |

Ordine OSPF: intra-area > inter-area > E1 > E2.

## 7. OSPF I vs OSPF II

| OSPF I | OSPF II |
|---|---|
| una sola area 0 | area 0 più tre aree stub |
| una LSDB per router | ABR con una LSDB per area |
| sole rotte intra-area | anche O IA e default stub |
| Type 1/2 centrali | Type 3, e negli avanzati Type 4/5 |
| nessun ABR | bb1 e bb2 ABR |
| studio DR/costi/SPF | studio isolamento LSDB, summary, stub e ASBR |

## 8. Ruoli da distinguere

- **Internal router:** tutte le interfacce OSPF nella stessa area.
- **Backbone router:** almeno un'interfaccia OSPF in area 0.
- **ABR:** backbone router collegato anche ad altre aree; mantiene più LSDB.
- **ASBR:** importa rotte esterne in OSPF; in `asbr-bgp` è bb3.

Un router può avere più ruoli: ogni ABR è anche backbone router, ma non ogni
backbone router è ABR.

## 9. Default route, stub e totally stubby

- Stub standard: niente Type 4/5; Type 3 specifiche ammesse; default Type 3.
- Stub no-summary: anche le Type 3 specifiche sono soppresse; resta default.
- La default stub è originata dall'ABR con costo iniziale 1 in FRR, configurabile
  tramite `area AREA default-cost N`.
- Un'area stub non può contenere un ASBR perché non accetta Type 5.

## 10. Cose da sapere all'orale in 5 minuti

1. Ogni area ha una LSDB separata e calcola la propria SPF.
2. Area 0 è il backbone; bb1 e bb2 sono gli ABR.
3. Type 1/2 descrivono la topologia locale; Type 3 porta raggiungibilità
   inter-area; Type 4 raggiungibilità dell'ASBR; Type 5 rotte esterne.
4. O = intra-area, O IA = inter-area, E1 somma costo esterno e interno, E2 usa
   soprattutto la metrica esterna.
5. Stub blocca Type 4/5 e riceve default; no-summary blocca anche le Type 3
   specifiche.
6. Cambiare costo crea nuova Type 1, flooding e SPF. Link-down locale è
   immediato; packet loss fa cadere il neighbor solo alla scadenza del Dead
   Timer.
7. Area 1 ha un solo ABR: perdere bb1-eth2 la isola, non esiste backup.
8. Nell'avanzato bb3 è ASBR: il backbone vede 50/16 come E2, r2 la raggiunge
   via default senza vedere la Type 5.

## 11. Incoerenze note del testo originale

- La topologia ufficiale ha anche area 3.3.3.3 e router r4-r6.
- Q9 cita correttamente `bb1 eth2`; il commento nascosto parla invece di
  `eth1` e di un ABR alternativo inesistente per area 1.
- Q10 indica `eth1`, ma il link bb1→area 1 è `eth2` (`eth3` va in area 2).
- Q6 modifica un costo uscente da bb0 ma chiede di osservare da r2: la
  direzionalità può lasciare invariato quel percorso.
- Q12 chiama `O` un router, ma O è il collision domain bb3-AS100r1.
- Il sample BGP non contiene la redistribuzione BGP→OSPF necessaria per una
  Type 5 E2 e non assegna 50.0.0.1 a un'interfaccia; `asbr-bgp/` completa
  entrambi i punti usando i valori già indicati dal laboratorio.

## 12. Validazione runtime eseguita

Test del 09/09/2026 con Kathará 3.8.0, Docker 28.5.2/OrbStack e
`kathara/frr:latest`:

- base: 11/11 router e 14/14 domini avviati; adiacenze attese tutte presenti;
  r2 con rotte O IA e default `[110/21]`; r3 con due default ECMP `[11]`;
  traceroute bb0→r2 e inverso conformi a Q4;
- backbone-rip: 11/11 router e 14/14 domini; RIP apprende le reti periferiche,
  r2 vede reti di area 3 come E2 metric 10; ping area 1↔area 3 con 0% loss;
- asbr-bgp: 12/12 router e 15/15 domini; eBGP Established, bb3 riceve 50/16,
  bb1 vede Type 5 E2 metric 20, r2 non vede Type 4/5 ma raggiunge 50.0.0.1
  tramite default; ping 0% loss e traceroute di cinque hop riuscito;
- tutti gli scenari sono stati rimossi con `kathara lclean` al termine.
