<script>
    import axios from "axios";

    let team_list = [];
    const get_teams = async () => {
        await axios
            .get(`http://localhost:8000/teams`)
            .then((res) => (team_list = res.data));
    };
</script>

<div class="page">
    <div class="page-title">Teams</div>
    <div class="content-container">
        <div class="container-title">Teams</div>
        <div class="content">
            <div class="selection-box">Select</div>
            <button on:click={() => get_teams()}> Get Teams </button>
            {#each team_list as team}
                <p>{team.teamname}:</p>
                <ul>
                    {#each team.users as user}
                        <li>{user.username}</li>
                    {/each}
                </ul>
            {/each}
        </div>
    </div>
</div>

<style>
    .selection-box {
        width: 100%;
        background-color: #333;
    }
</style>
