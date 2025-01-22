module.exports = {
  branches: ["main"],
  repositoryUrl: "https://github.com/plane-paper/KnowledgeHunt.git",
  plugins: [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    // [
    //   "@semantic-release/npm",
    //   {
    //     npmPublish: false,
    //   },
    // ],
    "@semantic-release/github",
    [
      "@semantic-release/git",
      {
        assets: ["package.json", "CHANGELOG.md"],
        message: "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}",
      },
    ],
  ],
};
