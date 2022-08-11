<script>
    import { Link } from "svelte-navigator";
</script>

<div class="topBar">
    <div class="title">Clock In Tool</div>
    <Link to="/">Home</Link>
    <Link to="/user">User</Link>
    <Link to="/clocks">Clock-In</Link>
    <Link to="/team">Teams</Link>
</div>

<style>
    .topBar {
        position: absolute;
        width: 100%;
        height: 80px;
        position: fixed;
        /* background: linear-gradient(90deg, var(--primary) 10%, var(--secondary) 100%); */
        background-color: var(--secondary);
        color: var(--text);
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;

        box-shadow: 0.1px 0.1px 0.1px 1px #ffffff;

        display: flex;
        align-items: center;
        justify-content: left;
        border-radius: 0 0 1% 1%;
        flex-direction: row;
        gap: 40px;
    }

    .title {
        font-size: 32px;
        padding: 20px;
        text-transform: uppercase;
    }
</style>
