from html import escape


MILESTONE_GROUPS = (
    ("land-and-tenure", "Land and tenure", (
        ("1878", "The racecourse and recreation reserve is gazetted", "whenua"),
        ("1914", "The club takes its first lease at Gate Pā", "first-lease"),
        ("1952", "The Reserve Board records a 25-year lease plus a further 25 years", "longer-leases"),
        ("1977", "The club takes a new 33-year lease", "longer-leases"),
        ("1989–1994", "Council takes over administration and establishes a new committee", "management"),
        ("2006", "The renewed lease term runs to 2039", "management"),
        ("2021", "The Greerton Maarawaewae Study begins", "beyond-2039"),
        ("2023", "Council approves entering into a long-term lease concession", "beyond-2039"),
    )),
    ("layout-and-access", "Course layout and access", (
        ("1956", "Crown purchase makes room to develop the third fairway", "shared-ground"),
        ("1960–1962", "The Reserve Board and clubs work to move race-day traffic off the course", "shared-ground"),
        ("1966", "The first stage of the golf car park proceeds", "shared-ground"),
        ("1980", "Realignment of the road around the ninth tee is approved", "ninth-hole"),
        ("1984", "The ninth hole and green redesign is approved", "ninth-hole"),
    )),
)


def course_milestones():
    groups = []
    for anchor, title, entries in MILESTONE_GROUPS:
        rows = "".join(
            f'<li><span class="year">{escape(year)}</span>'
            f'<div><a href="racecourse-reserve.html#{section}">{escape(event)}</a></div></li>'
            for year, event, section in entries
        )
        groups.append(
            f'<details class="timeline-era" id="{anchor}">'
            f'<summary>{escape(title)}</summary><ol class="timeline">{rows}</ol></details>'
        )
    return '<section class="story-period" id="course-milestones"><h2>Course milestones</h2>' + "".join(groups) + '</section>'


def reserve_feature():
    return """<section class="story-period" aria-labelledby="reserve-title">
    <a class="card reserve-feature" href="racecourse-reserve.html">
    <img src="assets/programme-1968-course-aerial.jpg" alt="" width="640" height="400">
    <div><h2 id="reserve-title">The Racecourse Reserve and the club’s lease</h2>
    <p>The story of Maarawaewae, the ground shared with racing, and the lease that made a permanent home possible.</p>
    <span class="read">Read the chapter →</span></div></a></section>"""


def build_reserve_chapter(page, heading):
    title = "The Racecourse Reserve and the club’s lease"
    body = """<div class="chapter-nav" role="navigation" aria-label="In this chapter">
    <a href="#whenua">The whenua</a><a href="#first-lease">The first lease</a>
    <a href="#shared-ground">Sharing the reserve</a><a href="#beyond-2039">Beyond 2039</a></div>
    <div class="article-layout"><article class="prose">
    <h2 id="whenua">Maarawaewae before golf</h2>
    <p>Maarawaewae was part of a landscape of gardens that fed local hapū and visitors from across the Bay of Plenty. Bonnie Whaeanui Pearson, drawing on a manuscript by her great-grandfather Te Haari Piahana, recalls food from these gardens sustaining tūpuna during the Tauranga Wars, including at Pukehinahina and Te Ranga.</p>
    <p>Following the fighting in 1864, the Crown confiscated the land as part of a much wider taking. The whenua chronology records that 200 acres were set aside in 1874 for a racecourse and recreation reserve. The reserve was gazetted in 1878 and made permanent as a domain in 1879.</p>
    <p class="source"><a href="https://letstalk.tauranga.govt.nz/projects/the-greerton-maarawaewae-study">Greerton Maarawaewae Study and its history of the whenua</a> · <a href="book-page-022.html">Pars from the Past, p. 22</a></p>
    <h2 id="first-lease">A home on Crown land</h2>
    <p>As the Domain became crowded with other sports, Tauranga Golf Club looked to the Racecourse Reserve. The club approached the trustees in 1913 and took up a lease in 1914. That arrangement gave members room to lay out eighteen holes, including some inside the racecourse oval. The land remained a Crown reserve. The club occupied part of it as a tenant alongside racing.</p>
    <p class="source"><a href="gate-pa.html">A new home at Gate Pa</a> · <a href="book-page-023.html">Pars from the Past, p. 23</a></p>
    <h2 id="longer-leases">Longer leases made investment possible</h2>
    <p>The original seven-year term gave the club limited certainty for spending on the course and buildings. Ernie Craig’s notes record a lease renewal in 1952 for 25 years plus a further 25 years, with a ten-year review and rent of £25. He records a new 33-year lease in 1977.</p>
    <p class="source">Ernie Craig, <cite>Moments in History</cite>, 8 May 2002, in the club history compilation, pp. 5, 7 · <a href="book-page-023.html">Pars from the Past, p. 23</a></p>
    <h2 id="shared-ground">Sharing the reserve changed the course</h2>
    <p>In 1956, the Crown bought a little over two hectares and added it to the land leased to the club so the third fairway could be developed. Race days also shaped how the course was used. Cars crossed fairways to reach parking, leaving ruts when the ground was wet. Craig records the closure of the gate by the fourteenth green and the move of race-day parking from the eighth and ninth fairways to McKinlay’s paddock in 1960. The book records a 1961 agreement and a breach in 1962, when cars again entered across the thirteenth fairway.</p>
    <p>The first stage of the golf car park proceeded in 1966. The entrance was reconstructed in 1974 and the shared road was widened and resealed in 1988, with Council contributing because soccer users also used it.</p>
    <h3 id="ninth-hole">The road and the ninth hole</h3>
    <p>The club approved moving the entry road in 1980 to separate golf from racing traffic, with the ninth tee to move forward. Funding took further negotiation. Craig records approval of the ninth hole and green redesign in 1984.</p>
    <p class="source">Craig, <cite>Moments in History</cite>, pp. 5–8 of the compilation · <a href="book-page-022.html">Pars from the Past, p. 22</a> · <a href="book-page-155.html">Entry road, p. 155</a></p>
    <h2 id="management">From trustees to Council</h2>
    <p>In 1989, reserve administration passed to Tauranga District Council. A new management committee began in January 1994, with Council, golf, racing, equestrian and soccer representation. Council’s reserve plan records a renewed lease term running from 2006 to 2039. In 2017, Council entered into a memorandum of understanding with the newly formed Tauranga Racecourse Reserve Charitable Trust.</p>
    <p class="source"><a href="book-page-024.html">Pars from the Past, p. 24</a> · <a href="https://www.tauranga.govt.nz/Portals/0/data/council/plans/reserve_management/files/tga_rmp/final_tauranga_rmp_reserve_specific_info.pdf">2019 Tauranga Reserves Management Plan</a></p>
    <h2 id="beyond-2039">Seeking certainty beyond 2039</h2>
    <p>When Council began the Greerton Maarawaewae Study in 2021, the long-term use of the reserve came up for public discussion. Council’s study papers record the club’s main lease over 45 hectares as running to 30 June 2039. In 2023, the club told Council it wanted certainty beyond that date and was open to a memorandum of understanding as a step towards early renewal.</p>
    <p>On 14 August 2023, Council resolved to enter into a new long-term lease concession with Tauranga Golf Club. The resolution provided for community access, connections to Kopurererua Valley and room for future infrastructure. As at November 2026, this chapter records the Council resolution and the club’s position. A signed replacement lease and its terms are yet to be confirmed for the heritage record.</p>
    <p class="source"><a href="https://www.sunlive.co.nz/news/279745-home-to-golf-and-racing-under-spotlight.html">SunLive, 26 October 2021</a> · <a href="https://infocouncil.tauranga.govt.nz/Open/2022/04/CO_20220411_AGN_2424_AT_files/CO_20220411_AGN_2424_AT_Attachment_11714_4.PDF">Council lease summary</a> · <a href="https://infocouncil.tauranga.govt.nz/Open/2023/05/CO_20230501_AGN_2555_AT.htm">Club submission recorded by Council</a> · <a href="https://infocouncil.tauranga.govt.nz/Open/2023/09/CO_20230904_AGN_2512_AT.htm">Council resolution CO13/23/5</a></p>
    <p><a href="course.html#course-milestones">← Course milestones</a></p></article>
    <aside><figure><a href="assets/programme-1968-course-aerial.jpg"><img src="assets/programme-1968-course-aerial.jpg" alt="Aerial view showing the golf course beside the racecourse oval and highway"></a>
    <figcaption>The golf course, racecourse and highway. <a href="documents/spalding-masters-1968-searchable.pdf#page=25">1968 Spalding Masters programme, printed p. 23</a>.</figcaption></figure>
    <div class="note"><h2>Explore the course</h2><p><a href="gate-pa.html">A new home at Gate Pa</a></p><p><a href="course-redesign.html">Beyond the racecourse oval</a></p><p><a href="course.html#course-milestones">Course milestones</a></p></div></aside></div>"""
    page(
        "racecourse-reserve.html", title,
        '<a class="back" href="course.html">← The Course</a>'
        + heading("MAARAWAEWAE · GREERTON", title,
                  "How the club made its home on a Crown reserve, and why the lease still matters.")
        + body,
    )
