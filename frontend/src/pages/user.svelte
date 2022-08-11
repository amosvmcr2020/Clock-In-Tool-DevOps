<script>
    import axios from "axios";

    let user_list = [];
    console.log(user_list);

    const get_users = async () => {
        await axios
            .get(`http://localhost:8000/users`)
            .then((res) => (user_list = res.data));
        console.log(user_list[0]);
    };

    let current_user;
</script>

<div class="page">
    <div class="page-title">User</div>
    <div class="content-container">
        <div class="content">
            {#if current_user}
                You are currently logged in as: {current_user}
                <button on:click={() => get_users()}>Change User</button>
            {:else}
                You are not currently logged in.
                <button on:click={() => get_users()}> Log in </button>
            {/if}
        </div>
        <div class="content">
            {#each user_list as user}
                <p>
                    {user.username}
                </p>
            {/each}
        </div>
    </div>
</div>

<style>
    .content {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 5%;
    }
</style>
