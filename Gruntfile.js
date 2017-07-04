module.exports = function(grunt) {

    grunt.loadNpmTasks('grunt-browserify')
    grunt.loadNpmTasks('grunt-watchify')

    var task = {
        options: {
            debug: true,
            transform: [['babelify', {presets: ['es2015', 'react']}]]
        },
        background: {
            src: './extension/background/scripts/background.js',
            dest: './extension/build/background.js'
        },
        mainpanel: {
            src: ['./extension/common/scripts/*.js',
                  './extension/background/scripts/*.js',
                  '!./extension/background/scripts/background.js'
                 ],
            dest: './extension/build/mainpanel.js'
        },
        content: {
            src: ['./extension/common/scripts/*.js',
                  './extension/content/scripts/*.js',
                  './extension/content/scripts/injected.js'
                 ],
            dest: './extension/build/content.js'
        }
    }

    grunt.initConfig({
        // manifest: grunt.file.readJSON('./extension/manifest.json'),
        browserify: task,
        watchify: task
    })

    grunt.registerTask('default', [
        'browserify',
    ])

    grunt.registerTask('watch', [
        'watchify'
    ])
}
