
import { useEffect, useState } from "react";

function HomePage() {
    const [myTeams, setMyTeams] = useState([]);
    const [exploreTeams, setExploreTeams] = useState([]);
    const [myRequests, setMyRequests] = useState([]);
    const [requestedTeamIds, setRequestedTeamIds] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [sendingTeamId, setSendingTeamId] = useState(null);

    // Fetch homepage data
    async function fetchHomeData() {
        try {
            const [myTeamsRes, exploreRes, requestsRes] =
                await Promise.all([
                    fetch("/api/my-teams/", {
                        credentials: "same-origin"
                    }),
                    fetch("/api/explore-teams/", {
                        credentials: "same-origin"
                    }),
                    fetch("/api/my-requests/", {
                        credentials: "same-origin"
                    })
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
            await fetch("/api/csrf/", {
                credentials: "same-origin"
            });

            const csrfToken = getCsrfToken();

            const response = await fetch("/api/send-request/", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    team_id: teamId
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Unable to send join request.");
            }

            // Change the button to Request Pending
            setRequestedTeamIds(previous => [
                ...previous,
                teamId
            ]);

            // Refresh the request list
            const requestsResponse = await fetch("/api/my-requests/", {
                credentials: "same-origin"
            });

            if (requestsResponse.ok) {
                const requestsData = await requestsResponse.json();
                setMyRequests(requestsData.requests || []);
            }

        } catch (err) {
            alert(err.message);
        } finally {
            setSendingTeamId(null);
        }
    }

    if (loading) {
        return <h2>Loading your workspace...</h2>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div style={{ padding: "30px" }}>

            <h1>Welcome to Your Workspace</h1>

            {/* MY TEAMS */}
            <section>
                <h2>My Teams</h2>

                {myTeams.length === 0 ? (
                    <p>You haven't joined any teams yet.</p>
                ) : (
                    myTeams.map(team => (
                        <div key={team.team_id}>
                            <h3>{team.team_name}</h3>
                            <p>{team.team_description}</p>
                        </div>
                    ))
                )}
            </section>

            <hr />

            {/* MY JOIN REQUESTS */}
            <section>
                <h2>My Join Requests</h2>

                {myRequests.length === 0 ? (
                    <p>You haven't sent any join requests.</p>
                ) : (
                    myRequests.map(request => (
                        <div key={request.id}>
                            <h3>{request.team_name}</h3>
                            <p>Status: {request.status}</p>
                        </div>
                    ))
                )}
            </section>

            <hr />

            {/* EXPLORE TEAMS */}
            <section>
                <h2>Explore Teams</h2>

                {exploreTeams.length === 0 ? (
                    <p>No teams available to join.</p>
                ) : (
                    exploreTeams.map(team => {
                        const requested = requestedTeamIds.includes(team.team_id);

                        return (
                            <div key={team.team_id}>
                                <h3>{team.team_name}</h3>
                                <p>{team.team_description}</p>

                                <small>
                                    Created: {new Date(team.created_at).toLocaleDateString()}
                                </small>

                                <br />

                                <button
                                    onClick={() => sendJoinRequest(team.team_id)}
                                    disabled={requested || sendingTeamId === team.team_id}
                                >
                                    {sendingTeamId === team.team_id
                                        ? "Sending..."
                                        : requested
                                            ? "Request Pending"
                                            : "Send Join Request"}
                                </button>
                            </div>
                        );
                    })
                )}
            </section>

        </div>
    );
}

export default HomePage;
