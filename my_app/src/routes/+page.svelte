<script lang="ts">
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';

    let recordings: any[] = [];
    let isRecording = false;
    let audioPlayer: HTMLAudioElement;
    let currentlyPlaying: string | null = null;

    onMount(() => {
        audioPlayer = new Audio();
        fetchRecordings();
    });

    async function fetchRecordings() {
        try {
            const response = await fetch('http://localhost:5000/api/recordings');
            recordings = await response.json();
        } catch (error) {
            console.error('Error fetching recordings:', error);
        }
    }

    async function startRecording() {
        try {
            isRecording = true;
            const response = await fetch('http://localhost:5000/api/record', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ duration: 5 })
            });
            const newRecording = await response.json();
            recordings = [newRecording, ...recordings];
        } catch (error) {
            console.error('Error recording:', error);
        } finally {
            isRecording = false;
        }
    }

    async function deleteRecording(id: string) {
        try {
            await fetch(`http://localhost:5000/api/recordings/${id}`, {
                method: 'DELETE'
            });
            recordings = recordings.filter(r => r.id !== id);
        } catch (error) {
            console.error('Error deleting recording:', error);
        }
    }

    function playRecording(id: string) {
        if (currentlyPlaying === id) {
            audioPlayer.pause();
            currentlyPlaying = null;
        } else {
            audioPlayer.src = `http://localhost:5000/api/recordings/${id}`;
            audioPlayer.play();
            currentlyPlaying = id;
        }
    }
</script>

<div class="container">
    <h1>Audio Recorder</h1>
    
    <div class="controls">
        <button 
            class="record-button" 
            on:click={startRecording} 
            disabled={isRecording}
        >
            {isRecording ? 'Recording...' : 'Record Audio'}
        </button>
    </div>

    <div class="recordings-list">
        {#each recordings as recording (recording.id)}
            <div class="recording-item" in:fade>
                <div class="recording-info">
                    <span class="recording-name">{recording.name}</span>
                    <span class="recording-date">{new Date(recording.created_at).toLocaleString()}</span>
                </div>
                <div class="recording-actions">
                    <button 
                        class="play-button" 
                        on:click={() => playRecording(recording.id)}
                    >
                        {currentlyPlaying === recording.id ? 'Stop' : 'Play'}
                    </button>
                    <button 
                        class="delete-button" 
                        on:click={() => deleteRecording(recording.id)}
                    >
                        Delete
                    </button>
                </div>
            </div>
        {/each}
    </div>
</div>

<style>
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }

    h1 {
        text-align: center;
        margin-bottom: 2rem;
    }

    .controls {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }

    .record-button {
        padding: 1rem 2rem;
        font-size: 1.2rem;
        background-color: #ff4444;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .record-button:hover {
        background-color: #cc0000;
    }

    .record-button:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }

    .recordings-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .recording-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background-color: #f5f5f5;
        border-radius: 4px;
    }

    .recording-info {
        display: flex;
        flex-direction: column;
    }

    .recording-name {
        font-weight: bold;
    }

    .recording-date {
        font-size: 0.8rem;
        color: #666;
    }

    .recording-actions {
        display: flex;
        gap: 0.5rem;
    }

    .play-button, .delete-button {
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .play-button {
        background-color: #4CAF50;
        color: white;
    }

    .play-button:hover {
        background-color: #45a049;
    }

    .delete-button {
        background-color: #f44336;
        color: white;
    }

    .delete-button:hover {
        background-color: #da190b;
    }
</style>