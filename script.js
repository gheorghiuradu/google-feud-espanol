// Google Feud Español - Game Logic

class GoogleFeudGame {
    constructor() {
        this.score = 0;
        this.currentRound = 1;
        this.guessesLeft = 4;
        this.currentQuestion = null;
        this.currentAnswers = [];
        this.revealedAnswers = [];
        this.gameData = {};
        this.selectedCategory = null;
        this.usedQuestions = new Set(); // Track used questions to prevent repeats

        this.init();
    } async init() {
        await this.loadGameData();
        this.setupEventListeners();
        this.updateDisplay();
    }

    async loadGameData() {
        try {
            const categories = ['cultura', 'personas', 'nombres', 'preguntas', 'animales', 'entretenimiento', 'comida'];

            for (const category of categories) {
                const response = await fetch(`data/${category}.json`);
                this.gameData[category] = await response.json();
            }
        } catch (error) {
            console.error('Error loading game data:', error);
            alert('Error cargando los datos del juego. Por favor, recarga la página.');
        }
    }

    setupEventListeners() {
        // Category selection
        $('.category-btn').on('click', (e) => {
            this.selectedCategory = $(e.target).data('category');
            this.startGame();
        });

        // Guess submission
        $('#submitGuess').on('click', () => this.submitGuess());
        $('#guessInput').on('keypress', (e) => {
            if (e.which === 13) { // Enter key
                this.submitGuess();
            }
        });

        // Game controls
        $('#nextRound').on('click', () => this.nextRound());
        $('#newGame').on('click', () => this.newGame());
        $('#playAgain').on('click', () => this.newGame());
    }

    startGame() {
        $('#categorySelection').hide();
        $('#gamePlay').show();
        this.loadNewQuestion();
    }

    loadNewQuestion() {
        if (!this.gameData[this.selectedCategory] || this.gameData[this.selectedCategory].length === 0) {
            alert('No hay preguntas disponibles para esta categoría.');
            return;
        }

        const questions = this.gameData[this.selectedCategory];

        // If we've used all questions, reset the used questions set
        if (this.usedQuestions.size >= questions.length) {
            this.usedQuestions.clear();
        }

        // Find available questions (not yet used)
        const availableQuestions = questions.filter((_, index) => !this.usedQuestions.has(index));

        // If no available questions, reset and use all questions
        const questionsToChooseFrom = availableQuestions.length > 0 ? availableQuestions : questions;

        // Select a random question from available questions
        const randomIndex = Math.floor(Math.random() * questionsToChooseFrom.length);
        const selectedQuestion = questionsToChooseFrom[randomIndex];

        // Find the original index of the selected question and mark it as used
        const originalIndex = questions.findIndex(q => q === selectedQuestion);
        this.usedQuestions.add(originalIndex);

        this.currentQuestion = selectedQuestion;
        this.currentAnswers = [...this.currentQuestion.answers]; // Copy array
        this.revealedAnswers = [];

        // Re-enable input for new question
        $('#guessInput').prop('disabled', false);
        $('#submitGuess').prop('disabled', false);

        // Update UI
        $('#question').text(this.currentQuestion.question);
        this.generateAnswersGrid();
        $('#guessInput').val('').focus();
        $('#nextRound').hide();
        $('#newGame').hide();
    }

    generateAnswersGrid() {
        const $grid = $('#answersGrid');
        $grid.empty();

        this.currentAnswers.forEach((answer, index) => {
            // Calculate points based on rank (1-10), with rank 1 = 10000 points, rank 10 = 1000 points
            const points = 11000 - (answer.rank * 1000);

            const $answerItem = $(`
                <div class="answer-item" data-index="${index}">
                    <span class="answer-text" style="visibility: hidden;">${answer.text}</span>
                    <span class="answer-points" style="visibility: hidden;">${points}</span>
                </div>
            `);
            $grid.append($answerItem);
        });
    }

    submitGuess() {
        const guess = $('#guessInput').val().trim().toLowerCase();

        if (!guess) {
            alert('Por favor, escribe una respuesta.');
            return;
        }

        this.processGuess(guess);
    }

    processGuess(guess) {
        // Don't process guess if no guesses left
        if (this.guessesLeft <= 0) {
            return;
        }

        let found = false;

        for (let i = 0; i < this.currentAnswers.length; i++) {
            const answer = this.currentAnswers[i];

            if (!this.revealedAnswers.includes(i) &&
                this.normalizeText(answer.text).includes(this.normalizeText(guess))) {

                this.revealAnswer(i, true);
                // Calculate points based on rank
                const points = 11000 - (answer.rank * 1000);
                this.score += points;
                found = true;
                break;
            }
        }

        if (!found) {
            this.guessesLeft--;
            this.showWrongAnswerFeedback();
            if (this.guessesLeft <= 0) {
                // Disable input when no guesses left
                $('#guessInput').prop('disabled', true);
                $('#submitGuess').prop('disabled', true);
                this.endRound();
            }
        }

        $('#guessInput').val('');
        this.updateDisplay();

        // Check if all answers are revealed
        if (this.revealedAnswers.length === this.currentAnswers.length) {
            this.endRound();
        }
    }

    showWrongAnswerFeedback() {
        // Create and show red X for wrong answer
        const $wrongX = $('<div class="wrong-answer-x">✗</div>');
        $('body').append($wrongX);

        // Animate fade out and remove
        $wrongX.animate({
            opacity: 0,
            fontSize: '6em'
        }, 800, function () {
            $(this).remove();
        });
    }

    normalizeText(text) {
        return text.toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '') // Remove accents
            .replace(/[^\w\s]/g, '') // Remove special characters
            .trim();
    }

    revealAnswer(index, correct) {
        this.revealedAnswers.push(index);
        const $answerItem = $(`.answer-item[data-index="${index}"]`);

        $answerItem.addClass('revealed');
        $answerItem.find('.answer-text, .answer-points').css('visibility', 'visible');
        if (correct) {
            $answerItem.addClass('correct');
        }
    }

    endRound() {
        // Reveal all remaining answers
        for (let i = 0; i < this.currentAnswers.length; i++) {
            if (!this.revealedAnswers.includes(i)) {
                this.revealAnswer(i, false);
            }
        }
        $('#nextRound').show();
    }

    nextRound() {
        this.currentRound++;
        this.guessesLeft = 4;
        this.updateDisplay();

        if (this.currentRound <= 3) {
            this.loadNewQuestion();
        } else {
            this.endGame();
        }
    }

    endGame() {
        $('#gamePlay').hide();
        $('#finalScore').text(this.score);
        $('#gameOver').show();
    }

    newGame() {
        this.score = 0;
        this.currentRound = 1;
        this.guessesLeft = 4;
        this.currentQuestion = null;
        this.currentAnswers = [];
        this.revealedAnswers = [];
        this.selectedCategory = null;
        this.usedQuestions.clear(); // Reset used questions for new game

        $('#gameOver').hide();
        $('#gamePlay').hide();
        $('#categorySelection').show();

        this.updateDisplay();
    } updateDisplay() {
        $('#score').text(this.score);
        $('#round').text(this.currentRound);
        $('#guesses').text(this.guessesLeft);
    }
}

// Initialize the game when the document is ready
$(document).ready(() => {
    new GoogleFeudGame();
});
