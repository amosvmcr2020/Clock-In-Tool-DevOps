<script>
    import axios from "axios";

    import { current_user_id } from "../store";

    export let alerts = [];

    let showModal = false;
    let login = true;

    let user_list = [];
    let team_list = [];

    const get_user = async (user_id) => {
        let user;
        await axios
            .get(`http://localhost:8000/user/${user_id}`)
            .then((res) => (user = res.data));
        return user;
    };

    const get_users = async () => {
        await axios
            .get(`http://localhost:8000/user`)
            .then((res) => (user_list = res.data));
    };

    const get_teams = async () => {
        await axios
            .get(`http://localhost:8000/team`)
            .then((res) => (team_list = res.data));
        team_list = team_list;
    };

    const toggleModal = async () => {
        await get_teams();
        showModal = !showModal;
    };

    const toggleLogin = async () => {
        login = !login;
    };

    const onSubmit = async (e) => {
        const formData = new FormData(e.target);

        const data = {};
        for (let field of formData) {
            const [key, value] = field;
            data[key] = value;
        }
        if (login) {
            try {
                await axios
                    .post(`http://localhost:8000/login`, {
                        username: data.username,
                        password: data.password,
                    })
                    .then((res) =>
                        current_user_id.update((val) => (val = res.data))
                    );
                alerts = alerts;
                window.location.reload();
            } catch (error) {
                alerts.push(["Error", error.response.data.detail]);
                alerts = alerts;
            }
        } else {
            await axios
                .post(`http://localhost:8000/user`, {
                    username: data.username,
                    password: data.password,
                    teamID: data.teamID,
                    hasAdmin: data.hasAdmin,
                })
                .then((res) =>
                    current_user_id.update((val) => (val = res.data.id))
                );
            window.location.reload();
        }
    };
</script>

<div class="page">
    <div class="page-title">User</div>
    <div class="content-container">
        <div class="content">
            {#if $current_user_id}
                {#await get_user($current_user_id)}
                    Loading...
                {:then user}
                    You are currently logged in as: {user.username}
                {/await}
                <button on:click={() => toggleModal()}>Change User</button>
            {:else}
                You are not currently logged in.
                <button on:click={() => toggleModal()}> Log in </button>
            {/if}
        </div>
        <div class="content">
            <button on:click={() => get_users()}> Get Users </button>
        </div>
        <div class="content">
            {#each user_list as user}
                <p>
                    {user.username}
                </p>
            {/each}
        </div>
    </div>
    {#if showModal}
        <div class="modal-container" />
        <div class="modal-window">
            <button class="close" on:click={() => toggleModal()}>X</button>
            {#if login}
                <div class="page-title">Log In</div>
                <div class="modalFormContainer">
                    <form class="modalForm" on:submit|preventDefault={onSubmit}>
                        <label for="username">Username</label>
                        <input
                            type="text"
                            name="username"
                            placeholder="Username"
                        />

                        <label for="password">Password</label>
                        <input
                            type="password"
                            name="password"
                            placeholder="Password"
                        />
                        <input class="end" type="submit" value="Submit" />
                    </form>
                    <br />
                    <div class="content bottom">
                        Want to create a new user?
                        <button on:click={() => toggleLogin()}>
                            Create User</button
                        >
                    </div>
                </div>
            {:else}
                <div class="page-title">Create User</div>
                <div class="modalFormContainer">
                    <form class="modalForm" on:submit|preventDefault={onSubmit}>
                        <label for="username">Username</label>
                        <input
                            type="text"
                            name="username"
                            placeholder="Username"
                        />

                        <input
                            type="password"
                            name="password"
                            placeholder="Password"
                        />

                        <label for="hasAdmin">Admin? </label>
                        <select name="hasAdmin" id="hasAdmin">
                            <option value="true">true</option>
                            <option selected="selected" value="false">
                                false
                            </option>
                        </select>

                        <label for="teamname">Team Name</label>
                        <select name="teamID" id="teamname">
                            {#each team_list as team}
                                <option value={team.id}>{team.teamname}</option>
                            {/each}
                        </select>

                        <input class="end" type="submit" value="Submit" />
                    </form>
                    <br />
                    <div class="content bottom">
                        Already have an account?
                        <button on:click={() => toggleLogin()}> Log In</button>
                    </div>
                </div>
            {/if}
        </div>
    {/if}
</div>

<style>
    .content {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 5%;
    }

    .end {
        align-self: end;
    }

    .bottom {
        padding-top: 10px;
        color: #333;
    }
</style>
