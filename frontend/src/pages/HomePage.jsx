import { useEffect, useState } from "react";

const styles = `
@import url("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;600;700;800&family=Instrument+Sans:wght@400;500;600;700&display=swap");

.page {
    --bg: #0c2e21;
    --surface: #123827;
    --surface-soft: #18432f;
    --ink: #f3ecd9;
    --ink-soft: #cdd9c8;
    --ink-faint: #9cb39a;
    --line: rgba(243, 236, 217, 0.14);
    --accent: #e34234;
    --accent-dark: #c02f22;
    --accent-soft: rgba(227, 66, 52, 0.16);
    --violet: #e8604f;
    --teal: #f3ecd9;
    --ok-bg: rgba(76, 175, 120, 0.18);
    --ok-fg: #8fd6a4;
    --wait-bg: rgba(240, 200, 100, 0.16);
    --wait-fg: #eac97e;
    --no-bg: rgba(227, 66, 52, 0.16);
    --no-fg: #f2937f;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.2);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.28);
    --shadow-lg: 0 16px 40px rgba(0, 0, 0, 0.4);
    --radius: 16px;

    min-height: 100vh;
    padding: 0 clamp(16px, 4vw, 48px) 72px;
    background:
        radial-gradient(900px 400px at 85% -100px, rgba(227, 66, 52, 0.18), transparent 70%),
        radial-gradient(700px 500px at 10% 110%, rgba(227, 66, 52, 0.1), transparent 70%),
        linear-gradient(180deg, #0e3626, #08251a);
    color: var(--ink);
    font-family: "Instrument Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
    line-height: 1.5;
    box-sizing: border-box;
}

.page *,
.page *::before,
.page *::after {
    box-sizing: border-box;
}

.page h1,
.page h2,
.page h3 {
    font-family: "Bricolage Grotesque", "Instrument Sans", system-ui, sans-serif;
    margin: 0;
    letter-spacing: -0.02em;
}

/* ---------- Hero header ---------- */

.hero {
    max-width: 1200px;
    margin: 0 auto 8px;
    padding: 64px 0 40px;
    position: relative;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 5px 14px 5px 10px;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(227, 66, 52, 0.2), rgba(227, 66, 52, 0.08));
    border: 1px solid rgba(227, 66, 52, 0.35);
    color: var(--accent);
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}

.hero-badge .dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: linear-gradient(135deg, var(--accent), var(--violet));
    box-shadow: 0 0 0 3px rgba(227, 66, 52, 0.25);
}

.hero h1 {
    margin: 16px 0 0;
    font-size: clamp(2.25rem, 5vw, 3.5rem);
    font-weight: 800;
    line-height: 1.08;
}

.hero h1 .grad {
    background: linear-gradient(100deg, var(--accent) 20%, var(--violet) 55%, var(--teal) 90%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    margin: 14px 0 0;
    max-width: 560px;
    color: var(--ink-soft);
    font-size: 1.1rem;
}

.hero-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 28px;
}

.stat {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 20px 12px 14px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: var(--shadow-sm);
}

.stat-icon {
    width: 38px;
    height: 38px;
    display: grid;
    place-items: center;
    border-radius: 10px;
    font-size: 1.05rem;
}

.stat-icon.indigo { background: var(--accent-soft); }
.stat-icon.amber { background: var(--wait-bg); }
.stat-icon.rose { background: var(--no-bg); }

.stat-value {
    color: var(--accent);
    font-family: "Bricolage Grotesque", sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    line-height: 1.1;
}

.stat-label {
    color: var(--ink-faint);
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}

/* ---------- Layout ---------- */

.layout {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: minmax(0, 1fr) 340px;
    gap: 36px;
    align-items: start;
}

.main-col {
    display: flex;
    flex-direction: column;
    gap: 48px;
}

.side-col {
    position: sticky;
    top: 24px;
}

/* ---------- Sections ---------- */

.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 18px;
}

.section-header h2 {
    font-size: 1.4rem;
    font-weight: 700;
}

.count {
    min-width: 26px;
    padding: 2px 9px;
    border-radius: 999px;
    background: var(--accent);
    color: #fff;
    font-size: 0.8rem;
    font-weight: 700;
    text-align: center;
}

/* ---------- Cards ---------- */

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
}

.card {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 14px;
    padding: 22px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    background:
        linear-gradient(180deg, rgba(243, 236, 217, 0.04), transparent 40%),
        var(--surface);
    box-shadow: var(--shadow-sm);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.card::before {
    content: "";
    position: absolute;
    inset: 0 0 auto 0;
    height: 4px;
    border-radius: var(--radius) var(--radius) 0 0;
    background: linear-gradient(90deg, var(--avatar-color, var(--accent)), transparent 140%);
    opacity: 0.95;
    height: 5px;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
    border-color: transparent;
}

.card-body {
    flex: 1;
}

.card h3 {
    font-size: 1.15rem;
    font-weight: 700;
}

.description {
    margin: 6px 0 0;
    color: var(--ink-soft);
    font-size: 0.95rem;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.meta {
    margin: 12px 0 0;
    padding-top: 10px;
    border-top: 1px solid var(--line);
    color: var(--ink-faint);
    font-size: 0.8rem;
}

.card-top {
    display: flex;
    align-items: center;
    gap: 14px;
}

.avatar {
    flex: none;
    width: 48px;
    height: 48px;
    display: grid;
    place-items: center;
    border-radius: 14px;
    color: var(--avatar-text, #fff);
    font-family: "Bricolage Grotesque", system-ui, sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.02em;
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.25), var(--shadow-md);
}

/* ---------- Buttons ---------- */

.btn {
    width: 100%;
    padding: 11px 18px;
    border: 1px solid transparent;
    border-radius: 12px;
    font: inherit;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.18s, border-color 0.18s, transform 0.18s, box-shadow 0.18s;
}

.btn:active:not(:disabled) {
    transform: scale(0.98);
}

.btn:focus-visible {
    outline: 3px solid rgba(227, 66, 52, 0.5);
    outline-offset: 2px;
}

.btn-primary {
    background: linear-gradient(135deg, var(--accent), var(--accent-dark));
    color: #fff;
    box-shadow: 0 6px 16px rgba(227, 66, 52, 0.45);
}

.btn-primary:hover:not(:disabled) {
    box-shadow: 0 10px 26px rgba(227, 66, 52, 0.55);
    transform: translateY(-1px);
}

.btn-primary:disabled {
    opacity: 0.75;
    cursor: progress;
}

.btn-ghost {
    background: var(--ok-bg);
    border-color: transparent;
    color: var(--ok-fg);
    cursor: default;
}

/* ---------- Side panel ---------- */

.panel {
    padding: 22px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    box-shadow: var(--shadow-md);
}

.request-list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
}

.request-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 13px 8px;
    margin: 0 -8px;
    border-radius: 12px;
    border-top: 1px solid var(--line);
    transition: background-color 0.15s;
}

.request-item:hover {
    background: rgba(243, 236, 217, 0.08);
}

.request-item:first-child {
    border-top: 0;
}

.request-item .avatar {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    font-size: 0.78rem;
    box-shadow: none;
}

.request-name {
    flex: 1;
    min-width: 0;
    font-weight: 500;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.badge {
    flex: none;
    padding: 4px 11px;
    border-radius: 999px;
    background: var(--line);
    color: var(--ink-soft);
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    text-transform: capitalize;
}

.badge-pending {
    background: var(--wait-bg);
    color: var(--wait-fg);
}

.badge-approved,
.badge-accepted {
    background: var(--ok-bg);
    color: var(--ok-fg);
}

.badge-rejected,
.badge-declined,
.badge-denied {
    background: var(--no-bg);
    color: var(--no-fg);
}

/* ---------- Empty states ---------- */

.empty {
    padding: 36px 24px;
    border: 1.5px dashed var(--line);
    border-radius: var(--radius);
    text-align: center;
    background: linear-gradient(135deg, rgba(243, 236, 217, 0.06), transparent);
}

.empty-icon {
    font-size: 1.6rem;
    margin-bottom: 10px;
    opacity: 0.8;
}

.empty p {
    margin: 0;
    font-weight: 600;
}

.empty.compact {
    padding: 20px 16px;
}

.muted {
    margin-top: 4px;
    color: var(--ink-faint);
    font-size: 0.9rem;
    font-weight: 400;
}

/* ---------- Error panel ---------- */

.error-panel {
    max-width: 480px;
    margin: 100px auto;
    padding: 36px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    box-shadow: var(--shadow-lg);
    text-align: center;
}

.error-panel .empty-icon {
    font-size: 2.2rem;
}

.error-panel h2 {
    margin-top: 12px;
    font-size: 1.4rem;
}

.error-panel p {
    margin: 8px 0 22px;
    color: var(--ink-soft);
}

.error-panel .btn {
    width: auto;
}

/* ---------- Toast ---------- */

.toast {
    position: fixed;
    right: 24px;
    bottom: 24px;
    max-width: calc(100vw - 48px);
    padding: 13px 20px 13px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-radius: 12px;
    background: var(--ink);
    color: #fff;
    font-weight: 500;
    box-shadow: var(--shadow-lg);
    animation: toast-in 0.3s cubic-bezier(0.21, 1.02, 0.73, 1);
}

.toast-icon {
    width: 22px;
    height: 22px;
    display: grid;
    place-items: center;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.18);
    font-size: 0.72rem;
}

.toast-success {
    background: linear-gradient(135deg, #4caf78, #2e7d4f);
}

.toast-error {
    background: linear-gradient(135deg, var(--accent), var(--accent-dark));
}

@keyframes toast-in {
    from {
        opacity: 0;
        transform: translateY(12px) scale(0.96);
    }
}

/* ---------- Skeletons ---------- */

.skeleton {
    border-radius: var(--radius);
    background: linear-gradient(90deg, #14392a 25%, #1a4632 50%, #14392a 75%);
    background-size: 200% 100%;
    animation: shimmer 1.4s infinite linear;
}

.skeleton-badge {
    width: 170px;
    height: 30px;
    border-radius: 999px;
    margin-bottom: 16px;
}

.skeleton-title {
    width: 420px;
    height: 52px;
    max-width: 100%;
    margin-bottom: 14px;
}

.skeleton-sub {
    width: 340px;
    height: 20px;
    max-width: 100%;
    margin-bottom: 32px;
}

.skeleton-stats {
    display: flex;
    gap: 12px;
    margin-bottom: 40px;
}

.skeleton-stats .skeleton {
    width: 150px;
    height: 64px;
}

.skeleton-card {
    height: 170px;
}

.skeleton-card.tall {
    height: 300px;
}

@keyframes shimmer {
    to {
        background-position: -200% 0;
    }
}

/* ---------- Utilities ---------- */

.fade-in {
    animation: fade-in 0.4s ease both;
}

@keyframes fade-in {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
}

.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0 0 0 0);
    white-space: nowrap;
}

@media (prefers-reduced-motion: reduce) {
    .skeleton,
    .toast,
    .fade-in {
        animation: none;
    }

    .btn,
    .card {
        transition: none;
    }

    .card:hover {
        transform: none;
    }
}

@media (max-width: 900px) {
    .hero {
        padding-top: 40px;
    }

    .layout {
        grid-template-columns: 1fr;
        gap: 40px;
    }

    .side-col {
        position: static;
 order: -1;
    }
}
`;

function Styles() {
    return <style>{styles}</style>;
}

// Pick a stable color for a team from its id/name
const AVATAR_COLORS = [
    "#E34234", "#F3ECD9", "#E8604F", "#4CAF78",
    "#C02F22", "#D9C9A3", "#2F5D45", "#F2937F"
];

function avatarColor(seed) {
    const str = String(seed ?? "");
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = (hash * 31 + str.charCodeAt(i)) % 9973;
    }
    return AVATAR_COLORS[hash % AVATAR_COLORS.length];
}

function initials(name = "") {
    return name
        .trim()
        .split(/\s+/)
        .slice(0, 2)
        .map(word => word[0]?.toUpperCase() || "")
        .join("") || "?";
}

function TeamAvatar({ id, name }) {
    const color = avatarColor(id ?? name);
    const light = ["#F3ECD9", "#D9C9A3", "#F2937F"].includes(color);

    return (
        <div
            className="avatar"
            style={{
                background: color,
                "--avatar-text": light ? "#0c2e21" : "#fff"
            }}
            aria-hidden="true"
        >
            {initials(name)}
        </div>
    );
}

function StatusBadge({ status }) {
    const key = String(status || "").toLowerCase();
    return <span className={`badge badge-${key}`}>{status}</span>;
}

function SectionHeader({ title, count }) {
    return (
        <div className="section-header">
            <h2>{title}</h2>
            {typeof count === "number" && <span className="count">{count}</span>}
        </div>
    );
}

function LoadingState() {
    return (
        <div className="page" aria-busy="true" aria-live="polite">
            <Styles />
            <div className="hero">
                <div className="skeleton skeleton-badge" />
                <div className="skeleton skeleton-title" />
                <div className="skeleton skeleton-sub" />
                <div className="skeleton-stats">
                    <div className="skeleton" />
                    <div className="skeleton" />
                    <div className="skeleton" />
                </div>
            </div>
            <div className="layout">
                <div className="main-col">
                    {[0, 1].map(i => (
                        <div key={i} className="skeleton skeleton-card" />
                    ))}
                </div>
                <div className="side-col">
                    <div className="skeleton skeleton-card tall" />
                </div>
            </div>
            <span className="sr-only">Loading your workspace…</span>
        </div>
    );
}

function HomePage() {
    const [myTeams, setMyTeams] = useState([]);
    const [exploreTeams, setExploreTeams] = useState([]);
    const [myRequests, setMyRequests] = useState([]);
    const [requestedTeamIds, setRequestedTeamIds] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [sendingTeamId, setSendingTeamId] = useState(null);
    const [toast, setToast] = useState(null);

    // Show a short-lived message
    function showToast(message, type = "error") {
        setToast({ message, type });
    }

    useEffect(() => {
        if (!toast) return;
        const timer = setTimeout(() => setToast(null), 4000);
        return () => clearTimeout(timer);
    }, [toast]);

    // Fetch homepage data
    async function fetchHomeData() {
        setLoading(true);
        setError("");

        try {
            const [myTeamsRes, exploreRes, requestsRes] =
                await Promise.all([
                    fetch("/api/my-teams/", { credentials: "same-origin" }),
                    fetch("/api/explore-teams/", { credentials: "same-origin" }),
                    fetch("/api/my-requests/", { credentials: "same-origin" })
                ]);

            if (!myTeamsRes.ok || !exploreRes.ok || !requestsRes.ok) {
                throw new Error("Failed to fetch homepage data.");
            }

            const myTeamsData = await myTeamsRes.json();
            const exploreData = await exploreRes.json();
            const requestsData = await requestsRes.json();

            setMyTeams(myTeamsData.teams || []);
            setExploreTeams(exploreData.teams || []);
            setMyRequests(requestsData.requests || []);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        fetchHomeData();
    }, []);

    // Get CSRF token from browser cookie
    function getCsrfToken() {
        const cookie = document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="));

        return cookie ? cookie.split("=")[1] : "";
    }

    // Send join request
    async function sendJoinRequest(teamId) {
        setSendingTeamId(teamId);

        try {
            // Ensure Django has issued a CSRF cookie
            await fetch("/api/csrf/", { credentials: "same-origin" });

            const csrfToken = getCsrfToken();

            const response = await fetch("/api/send-request/", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ team_id: teamId })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Unable to send join request.");
            }

            // Change the button to Request Pending
            setRequestedTeamIds(previous => [...previous, teamId]);
            showToast("Join request sent.", "success");

            // Refresh the request list
            const requestsResponse = await fetch("/api/my-requests/", {
                credentials: "same-origin"
            });

            if (requestsResponse.ok) {
                const requestsData = await requestsResponse.json();
                setMyRequests(requestsData.requests || []);
            }
        } catch (err) {
            showToast(err.message, "error");
        } finally {
            setSendingTeamId(null);
        }
    }

    if (loading) {
        return <LoadingState />;
    }

    if (error) {
        return (
            <div className="page">
                <Styles />
                <div className="error-panel" role="alert">
                    <div className="empty-icon" aria-hidden="true">⚠️</div>
                    <h2>We couldn't load your workspace</h2>
                    <p>{error}</p>
                    <button className="btn btn-primary" onClick={fetchHomeData}>
                        Try again
                    </button>
                </div>
            </div>
        );
    }

    const pendingRequests = myRequests.filter(
        request => String(request.status || "").toLowerCase() === "pending"
    ).length;

    return (
        <div className="page">
            <Styles />

            <header className="hero">
                <span className="hero-badge">
                    <span className="dot" aria-hidden="true" />
                    Team Workspace
                </span>
                <h1>
                    Good to see you. <span className="grad">Let's build together.</span>
                </h1>
                <p>
                    {myTeams.length === 0
                        ? "You're not in a team yet — explore the teams below and send a join request to get started."
                        : `You're collaborating across ${myTeams.length} ${myTeams.length === 1 ? "team" : "teams"}. Pick up where you left off, or discover something new.`}
                </p>

                <div className="hero-stats">
                    <div className="stat">
                        <span className="stat-icon indigo" aria-hidden="true">👥</span>
                        <div>
                            <div className="stat-value">{myTeams.length}</div>
                            <div className="stat-label">My teams</div>
                        </div>
                    </div>
                    <div className="stat">
                        <span className="stat-icon amber" aria-hidden="true">⏳</span>
                        <div>
                            <div className="stat-value">{pendingRequests}</div>
                            <div className="stat-label">Pending</div>
                        </div>
                    </div>
                    <div className="stat">
                        <span className="stat-icon rose" aria-hidden="true">🚀</span>
                        <div>
                            <div className="stat-value">{exploreTeams.length}</div>
                            <div className="stat-label">To explore</div>
                        </div>
                    </div>
                </div>
            </header>

            <div className="layout fade-in">
                <div className="main-col">
                    {/* MY TEAMS */}
                    <section aria-labelledby="my-teams-title">
                        <SectionHeader title="My teams" count={myTeams.length} />

                        {myTeams.length === 0 ? (
                            <div className="empty">
                                <div className="empty-icon" aria-hidden="true">🧩</div>
                                <p>You haven't joined any teams yet.</p>
                                <p className="muted">
                                    Pick a team below and send a join request.
                                </p>
                            </div>
                        ) : (
                            <div className="grid">
                                {myTeams.map(team => (
                                    <article
                                        key={team.team_id}
                                        className="card"
                                        style={{ "--avatar-color": avatarColor(team.team_id ?? team.team_name) }}
                                    >
                                        <div className="card-top">
                                            <TeamAvatar id={team.team_id} name={team.team_name} />
                                            <h3>{team.team_name}</h3>
                                        </div>
                                        <div className="card-body">
                                            <p className="description">{team.team_description}</p>
                                        </div>
                                        <p className="meta">
                                            Joined · active workspace
                                        </p>
                                    </article>
                                ))}
                            </div>
                        )}
                    </section>

                    {/* EXPLORE TEAMS */}
                    <section aria-labelledby="explore-title">
                        <SectionHeader title="Explore teams" count={exploreTeams.length} />

                        {exploreTeams.length === 0 ? (
                            <div className="empty">
                                <div className="empty-icon" aria-hidden="true">🔭</div>
                                <p>No teams available to join right now.</p>
                                <p className="muted">Check back later for new teams.</p>
                            </div>
                        ) : (
                            <div className="grid">
                                {exploreTeams.map(team => {
                                    const requested = requestedTeamIds.includes(team.team_id);
                                    const sending = sendingTeamId === team.team_id;

                                    return (
                                        <article
                                            key={team.team_id}
                                            className="card"
                                            style={{ "--avatar-color": avatarColor(team.team_id ?? team.team_name) }}
                                        >
                                            <div className="card-top">
                                                <TeamAvatar id={team.team_id} name={team.team_name} />
                                                <h3>{team.team_name}</h3>
                                            </div>
                                            <div className="card-body">
                                                <p className="description">{team.team_description}</p>
                                                <p className="meta">
                                                    Created{" "}
                                                    {new Date(team.created_at).toLocaleDateString(undefined, {
                                                        year: "numeric",
                                                        month: "short",
                                                        day: "numeric"
                                                    })}
                                                </p>
                                            </div>
                                            <button
                                                className={`btn ${requested ? "btn-ghost" : "btn-primary"}`}
                                                onClick={() => sendJoinRequest(team.team_id)}
                                                disabled={requested || sending}
                                            >
                                                {sending
                                                    ? "Sending…"
                                                    : requested
                                                        ? "✓ Request pending"
                                                        : "Send join request"}
                                            </button>
                                        </article>
                                    );
                                })}
                            </div>
                        )}
                    </section>
                </div>

                {/* MY JOIN REQUESTS */}
                <aside className="side-col" aria-labelledby="requests-title">
                    <div className="panel">
                        <SectionHeader title="My join requests" count={myRequests.length} />

                        {myRequests.length === 0 ? (
                            <div className="empty compact">
                                <div className="empty-icon" aria-hidden="true">📮</div>
                                <p>No requests sent yet.</p>
                                <p className="muted">
                                    Requests you send will show up here.
                                </p>
                            </div>
                        ) : (
                            <ul className="request-list">
                                {myRequests.map(request => (
                                    <li key={request.id} className="request-item">
                                        <TeamAvatar
                                            id={request.team_id ?? request.team_name}
                                            name={request.team_name}
                                        />
                                        <span className="request-name">{request.team_name}</span>
                                        <StatusBadge status={request.status} />
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                </aside>
            </div>

            {toast && (
                <div className={`toast toast-${toast.type}`} role="status" aria-live="polite">
                    <span className="toast-icon" aria-hidden="true">
                        {toast.type === "success" ? "✓" : "!"}
                    </span>
                    {toast.message}
                </div>
            )}
        </div>
    );
}

export default HomePage;
