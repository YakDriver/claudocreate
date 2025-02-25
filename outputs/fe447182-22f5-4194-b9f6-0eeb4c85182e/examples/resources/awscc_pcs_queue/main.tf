resource "awscc_pcs_queue" "example" {
  name       = "example-queue"
  cluster_id = "cluster-1234567890"

  tags = [{
    key   = "Modified By"
    value = "AWSCC"
  }]
}