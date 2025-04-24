// Base API URL (parameterized for better maintainability)
const API_BASE_URL = "https://jsonplaceholder.typicode.com"

// Function to calculate the sum of an array (using reduce for better readability)
function calculateSum(array) {
  if (!Array.isArray(array)) {
    throw new TypeError("Input must be an array of numbers.")
  }
  return array.reduce((sum, num) => sum + num, 0)
}

// Function to fetch user data from an API with error handling
async function fetchUserData(userId) {
  try {
    const url = `${API_BASE_URL}/users/${userId}`
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`API call failed with status ${response.status}`)
    }
    const data = await response.json()
    console.log("User Data:", data)
    return data
  } catch (error) {
    console.error("Error fetching user data:", error.message)
    return null
  }
}

// Function to format a user's full name safely
function formatFullName(user) {
  if (
    !user ||
    typeof user.firstName !== "string" ||
    typeof user.lastName !== "string"
  ) {
    console.warn("Invalid user object. Returning 'Unknown User'.")
    return "Unknown User"
  }
  return `${user.firstName} ${user.lastName}`
}

// Function to process multiple users and calculate their total ID sum
async function processUsers(userIds) {
  const results = []
  for (const userId of userIds) {
    const user = await fetchUserData(userId)
    if (user) {
      const fullName = formatFullName(user)
      console.log("Processed User:", fullName)
      results.push({ id: user.id, fullName })
    }
  }
  const totalIdSum = calculateSum(results.map((user) => user.id))
  console.log("Total User ID Sum:", totalIdSum)
  return results
}

// Test the functions
;(async () => {
  try {
    const users = await processUsers([1, 2, 3])
    console.log("Processed Users:", users)
  } catch (error) {
    console.error("Unexpected error during processing:", error.message)
  }
})()
