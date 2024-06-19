<template>
    <v-container>
        <v-row class="text-center">
            <v-col>
                <v-btn icon @click="goBack">
                    <v-icon>mdi-arrow-left</v-icon>
                </v-btn>
            </v-col>
        </v-row>
        <v-row class="text-center">
            <v-col>
                <h1>How would you like to build your resume?</h1>
            </v-col>
        </v-row>
        <v-row class="text-center">
            <v-col cols="12" md="6">
                <v-card class="pa-5" @click="createNewResume">
                    <v-icon size="48px" class="mb-4" color="green">mdi-plus-box</v-icon>
                    <h3>Start with a new resume</h3>
                    <p>Get step-by-step support with expert content suggestions at your fingertips!</p>
                    <v-btn color="primary" class="mt-4">Create new</v-btn>
                </v-card>
            </v-col>
            <v-col cols="12" md="6">
                <v-card class="pa-5" @click="triggerFileUpload">
                    <v-icon size="48px" class="mb-4" color="blue">mdi-upload</v-icon>
                    <h3>Upload an existing resume</h3>
                    <p>Edit your resume using expertly generated content in a fresh, new design.</p>
                    <v-btn color="warning" class="mt-4">Choose file</v-btn>
                    <input type="file" ref="fileInput" class="d-none" @change="handleFileUpload" />
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    methods: {
        goBack() {
            this.$router.go(-1);
        },
        createNewResume() {
            // Logic to start a new resume
        },
        triggerFileUpload() {
            this.$refs.fileInput.click();
        },
        handleFileUpload(event) {
            const file = event.target.files[0];
            const reader = new FileReader();

            reader.onload = () => {
                localStorage.setItem('uploadedResume', reader.result);
            };

            reader.readAsDataURL(file);
        }
    }
};
</script>

<style scoped>
.v-card {
    cursor: pointer;
    transition: transform 0.2s;
}

.v-card:hover {
    transform: scale(1.05);
}

@media (max-width: 600px) {
    .v-card {
        margin-bottom: 20px;
    }
}

@media (min-width: 600px) and (max-width: 960px) {
    .v-card {
        margin-bottom: 20px;
    }
}
</style>