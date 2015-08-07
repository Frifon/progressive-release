module.exports = function (grunt) {
    grunt.initConfig({
        less: {
          development: {
            files: {
              "static/build/styles.css": "static/styles.less"
            }
          }
        },
        autoprefixer: {
            dist: {
                files: {
                    'static/build/styles.prefixed.css': 'static/build/styles.css'
                }
            }
        },
        watch: {
            styles: {
                files: ['static/styles.less'],
                tasks: ['less', 'autoprefixer']
            }
        }
    });
    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');
};
